"""
Main processing functions ImageProcessing and TextProcessing
"""
import time
import cv2
import utils

class Image(object):
    """Image Class Processing
    Input: .TXT containing path to source image 
    Output: .TXT containing path to processed image 
    """
    def __init__(self, src, dst, *args, **kwargs):
        self.src = src
        self.dst = dst
        self.logger = utils.Log().create_logger(self.__class__.__name__)
        self.year = utils.Metadata(self.src).get_year()
        self.page = utils.Metadata(self.src).get_page()

        self.logger = utils.Log().create_logger(self.__class__.__name__)

    def selection(self, TRIGGER_ANALYZE):
        '''Returns a list of images paths to process'''

        # initialization
        img = cv2.imread(str(self.src))
        # preprocessing
        blur = utils.Remove().noise(img)
        gray = utils.Color().to_gray(blur)

        # detect lines with Canny thresholding method
        thresh = cv2.Canny(gray, 0, 255, apertureSize=3, L2gradient=True)

        # dilate and erode for better results at Houghlines transform stage
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 4))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

        # houghlinesP to estimate the number of edges
        lines = utils.Lines().houghlinesP(close)

        # analyze() returns a list of files to process
        document = utils.Should().analyze(self.src, TRIGGER_ANALYZE, self.year, self.page, lines)

        if document is not None:
            output = self.src
        else:
            output = None

        #draw HoughlinesP for debugging
        cimg = img.copy()
        draw_houghline = utils.Draw(cimg).draw_lines(lines)

        #write
        cv2.imwrite(
            str(self.dst / 'houghlineP_{:s}-{:s}.png').format(self.year, self.page), draw_houghline
        )

        return output

    def clean(self):
        '''Returns an image without any noise, skew angle, table lines, etc.'''
       
        # start timer
        start_timer = time.time()
        # display start
        self.logger.info('\033[1m Preprocess {:s} \033[0m'.format(str(self.src)))

        # load image
        img = cv2.imread(str(self.src))

        # Gaussian blur (5x5 kernel)
        self.logger.debug("\t > remove noise")
        blur = utils.Remove().noise(img)

        # grayscale
        self.logger.debug("\t > grayscale")
        gray = utils.Color().to_gray(blur)

        # otsu binarization
        self.logger.debug("\t > binarize")
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # estimate skewness angle
        angle = utils.Transform().estimate_angle(thresh)
        self.logger.debug("\t > skew angle = {:.2f} degree(s)".format(float(angle)))

        # rotate
        rotate = utils.Transform().rotate(thresh, angle)
        self.logger.debug("\t > rotate document by {:.2f} degree(s)".format(float(angle)))

        # remove lines
        self.logger.debug("\t > find lines")
        mask = utils.Lines().find_lines(rotate)

        # remove lines from the binarized image
        self.logger.debug("\t > remove lines")
        preprocessed = cv2.subtract(rotate, mask)
        preprocessed = cv2.bitwise_not(preprocessed)

        # stop timer
        stop_timer = time.time() - start_timer
        self.logger.info('\t Terminated - Lines removed in {:d} seconds.\n'.format(int(stop_timer)))

        # store output
        # output = [
        #     self.dst+"preprocessed_{:s}-{:s}.png".format(year, page),
        #     year,
        #     page
        # ]

        #opencv only accepts string as input
        cv2.imwrite(
            str(self.dst / "thresh_y{:s}-p{:s}.png").format(self.year, self.page),
            thresh
        )
        cv2.imwrite(
            str(self.dst / "rotate_y{:s}-p{:s}.png").format(self.year, self.page),
            rotate
        )
        cv2.imwrite(
            str(self.dst / "table_edges_y{:s}-p{:s}.png").format(self.year, self.page),
            mask
        )
        cv2.imwrite(
            str(self.dst / "preprocess_y{:s}-p{:s}.png").format(self.year, self.page),
            preprocessed
        )

        #output format is Posix
        output = self.dst / "preprocess_y{:s}-p{:s}.png".format(self.year, self.page)

        return output

    def block_segmentation(self):
        '''
        Segments an image into blocks and returns paths to segmented images.
        
        Returns:
            list[str]: Paths to segmented block images
        '''
        start_timer = time.time()
        self.logger.info(f" \033[1mStarting - Blocks segmentation of {self.src} \033[0m")

        img = cv2.imread(str(self.src))
        if img is None:
            self.logger.error(f"Failed to load image: {self.src}")
            return []

        # Preprocessing
        gray = utils.Color().to_gray(img)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Segment blocks
        self.logger.debug('\t > segment blocks')
        segment = utils.Segment().segment_block(thresh)
        contours, _ = cv2.findContours(segment, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        self.logger.info(f'\t > {len(contours)} blocks found.')

        # Process contours
        output = []
        count_blocks_kept = 0
        
        for i, cnt in enumerate(contours):
            area = int(cv2.contourArea(cnt))
            if area < 100000:
                continue
                
            self.logger.info(f'\t\t > {i}-th block considered (area = {area})')
            block_img = self._extract_block(img, cnt)
            
            if block_img is not None:
                filename = f"block_y{self.year}-p{self.page}-b{i}.png"
                cv2.imwrite(str(self.dst / filename), block_img)
                output.append(str(self.dst / filename))
                count_blocks_kept += 1

        # Write debug images
        cv2.imwrite(str(self.dst / f"blocks_thresh_y{self.year}-p{self.page}.png"), thresh)
        cv2.imwrite(str(self.dst / f"blocks_segmentation_y{self.year}-p{self.page}.png"), segment)

        stop_timer = time.time() - start_timer
        self.logger.info(
            f'\tTerminated - {len(output)} blocks segmented in {int(stop_timer)} seconds - {count_blocks_kept} considered.\n'
        )

        return output

    def line_segmentation(self):
        '''
        Segments blocks into lines and returns paths to segmented images.
        
        Returns:
            list[str]: Paths to segmented line images
        '''
        nth_block = utils.Metadata(self.src).get_block()
        start_timer = time.time()
        
        self.logger.info(f" \033[1mStarting - Line segmentation in {self.src} \033[0m")

        img = cv2.imread(str(self.src))
        if img is None:
            self.logger.error(f"Failed to load image: {self.src}")
            return []

        # Preprocessing
        gray = utils.Color().to_gray(img)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        segment = utils.Segment().segment_line(thresh)
        contours, _ = cv2.findContours(segment, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        output = []
        for i, cnt in enumerate(contours):
            area = int(cv2.contourArea(cnt))
            if area < 5000:
                continue

            self.logger.info(f'\t\t > {i}-th line considered (area = {area})')
            line_img = self._extract_line(img, cnt)
            
            if line_img is not None:
                mask_clean, line_clean = utils.Remove().artifacts(line_img['image'], line_img['height'])
                
                filename = f"line_y{self.year}-p{self.page}-b{nth_block}-r{i}.png"
                maskname = f"mask_y{self.year}-p{self.page}-b{nth_block}-r{i}.png"
                
                cv2.imwrite(str(self.dst / filename), line_clean)
                cv2.imwrite(str(self.dst / maskname), mask_clean)
                output.append(str(self.dst / filename))

        stop_timer = time.time() - start_timer
        self.logger.info(
            f'\t> Terminated - line segmentation for lines in block {nth_block} terminated in {int(stop_timer)} seconds.\n'
        )

        return output

    def _extract_block(self, img, contour, margin_x=20, margin_y=20):
        '''Helper method to extract a block from an image with margins'''
        x, y, w, h = cv2.boundingRect(contour)
        return self._extract_region(img, x, y, w, h, margin_x, margin_y)

    def _extract_line(self, img, contour, margin_x=40, margin_y=20):
        '''Helper method to extract a line from an image with margins'''
        x, y, w, h = cv2.boundingRect(contour)
        image = self._extract_region(img, x, y, w, h, margin_x, margin_y)
        return {'image': image, 'height': h} if image is not None else None

    def _extract_region(self, img, x, y, w, h, margin_x, margin_y):
        '''Helper method to extract a region from an image with margins and boundary checking'''
        start_x = max(0, x - margin_x)
        start_y = max(0, y - margin_y)
        end_x = min(img.shape[1], x + w + margin_x)
        end_y = min(img.shape[0], y + h + margin_y)
        
        if start_x >= end_x or start_y >= end_y:
            return None
            
        return img[start_y:end_y, start_x:end_x]