from base import Base_Handler
import tornado
from util.dbtool import *

from util.marcos import IMAGE_NUMBER_FOR_PAGE

class Browser_Handler(Base_Handler):
    def get(self):



        positions = []

        positions = get_positions()

        current_position = self.get_argument('position', '')
        current_page = self.get_argument('page', '')
        if current_page:
            current_page = int(current_page)
        else:
            current_page = 1
        if current_position:
            current_position_id = current_position
        else:
            # positions = position.get_position_by_device_id(devices[0].id)
            if positions:
                current_position = positions[0]['position']
            else:
                current_position = 0
        total_image_num = get_images_count(current_position)
        total_page_num = total_image_num/IMAGE_NUMBER_FOR_PAGE+1
        start_image_num = (current_page - 1)*IMAGE_NUMBER_FOR_PAGE + 1

        if total_page_num < current_page:
            current_page = total_page_num

        images = get_images(IMAGE_NUMBER_FOR_PAGE, (current_page - 1)*IMAGE_NUMBER_FOR_PAGE, current_position)

        # get the start and end page num
        if current_page > 3:
            start_page_num = current_page-3
        else:
            start_page_num = 1

        end_page_num = start_page_num+6
        if end_page_num>total_page_num:
            end_page_num = total_page_num
            start_page_num = end_page_num-6
            if start_page_num<1:
                start_page_num = 1

        end_image_num  = start_image_num+len(images)-1

        return self.render('browser.html',
                           page_name='browser',
                           positions=positions,
                           current_position=current_position,
                           current_page=current_page,
                           total_page_num=total_page_num,
                           total_image_num=total_image_num,
                           start_image_num=start_image_num,
                           end_image_num=end_image_num,
                           start_page_num=start_page_num,
                           end_page_num=end_page_num,
                           images=images
                           )