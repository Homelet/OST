from PIL import Image, ImageDraw, ImageFont

from Launcher import *
from OST_helper.data_handler import Data

TFONT = "./resource/times-new-roman.ttf"

default_coordinates = {
    "Size": (3300, 2532),
    "Offset": (0, 0),
    # (x, y, width, height)
    "OST_DateOfIssue": (2309, 91, 508, 89, 55),
    "Page_1": (2822, 91, 177, 89, 50),
    "Page_2": (3031, 91, 177, 89, 50),
    "Surname": (164, 221, 619, 89, 50),
    "GivenName": (783, 221, 755, 89, 50),
    "OEN": (1538, 221, 518, 89, 50),
    "StudentNumber": (2056, 221, 524, 89, 50),
    "Gender": (2580, 221, 134, 89, 50),
    "DateOfBirth_Y": (2714, 248, 195, 62, 40),
    "DateOfBirth_M": (2909, 248, 196, 62, 40),
    "DateOfBirth_D": (3105, 248, 139, 62, 40),
    "NameOfDSB": (148, 352, 1009, 93, 50),
    "NumberOfDSB": (1157, 352, 381, 93, 50),
    "NameOfSchool": (1538, 352, 789, 93, 50),
    "NumberOfSchool": (2327, 352, 387, 93, 50),
    "DateOfEntry_Y": (2714, 378, 195, 67, 40),
    "DateOfEntry_M": (2909, 378, 196, 67, 40),
    "DateOfEntry_D": (3105, 378, 139, 67, 40),
    # (x, y, width, height)
    "Course": (111, 572, 3134, 1363),
    # (x_offset, width)
    "Course_date_offset": (0, 261),
    "Course_level_offset": (264, 177),
    "Course_title_offset": (444, 1589),
    "Course_code_offset": (2036, 236),
    "Course_percentage_offset": (2275, 171),
    "Course_credit_offset": (2452, 180),
    "Course_compulsory_offset": (2635, 201),
    "Course_note_offset": (2842, 292),
    "SummaryOfCredit": (2567, 1941, 176, 66, 55),
    "SummaryOfCompulsory": (2746, 1941, 201, 66, 55),
    "CommunityInvolvement_True": (148, 2068),
    "CommunityInvolvement_False": (449, 2068),
    "ProvincialSecondarySchoolLiteracy_True": (680, 2068),
    "ProvincialSecondarySchoolLiteracy_False": (1215, 2068),
    "SpecializedProgram": (1494, 2049, 1750, 89, 40),
    "DiplomaOrCertificate": (129, 2187, 1578, 64, 40),
    "DiplomaOrCertificate_DateOfIssue_Y": (1734, 2213, 168, 52, 40),
    "DiplomaOrCertificate_DateOfIssue_M": (1911, 2213, 168, 52, 40),
    "Authorization": (2106, 2180, 1092, 85, 40),
}

# alignment flag
flag_left = 0
flag_center = 1
flag_right = 2

# checkMark
checkMark = Image.open("./resource/checkMark.png")
DEFAULT_COORDINATES_PATH = "./resource/default_coordinates.json"

try:
    coordinates = from_json(DEFAULT_COORDINATES_PATH)
    print("Loaded coordinates!")
except Exception as exp:
    print(
        "No default coordinates found, restoring from default..., Error: {}".format(
            str(exp)))
    coordinates = default_coordinates


def finalize():
    to_json(DEFAULT_COORDINATES_PATH, coordinates)
    print("Coordinates saved!")


def get_total_size_in_mm():
    width, height = coordinates["Size"]
    mm_width, mm_height = round(width * 0.264583), round(height * 0.264583)
    return mm_width, mm_height


def draw(info: Data.OST_info, draw_ost_template, offset=coordinates["Offset"],
         font=TFONT):
    course_images = draw_courses(courses=info.course(), font=font,
                                 font_size=info.course_font_size(),
                                 spacing=info.course_spacing())
    if draw_ost_template:
        from OST_helper.UI import OST_SAMPLE
        ost_template = Image.open(OST_SAMPLE)
    else:
        ost_template = None
    total_page = len(course_images)
    images = []
    full_name = info.full_name()
    for page_index in range(total_page):
        image = course_images[page_index]
        img = Image.new(mode="RGBA", size=coordinates["Size"],
                        color=(0, 0, 0, 0))
        drawer = ImageDraw.Draw(img)
        if draw_ost_template:
            template = ost_template.copy()
            draw_image(img, template, config=(0, 0), offset=(0, 0))
        # draw the courses
        course_x, course_y, _, _ = coordinates["Course"]
        draw_image(img, image, config=(course_x, course_y), offset=offset)
        # draw credit summary
        draw_text(drawer=drawer,
                  text=str(info.count_course_credit()),
                  config=coordinates["SummaryOfCredit"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_center)
        # draw compulsory summary
        draw_text(drawer=drawer,
                  text=str(info.count_course_compulsory()),
                  config=coordinates["SummaryOfCompulsory"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_center)
        # draw page number
        draw_text(drawer=drawer,
                  text=str(page_index + 1),
                  config=coordinates["Page_1"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_center)
        draw_text(drawer=drawer,
                  text=str(total_page),
                  config=coordinates["Page_2"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_center)
        # draw OST Date of Issue
        draw_text(drawer=drawer,
                  text=info.OST_date_of_issue(),
                  config=coordinates["OST_DateOfIssue"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw Surname
        draw_text(drawer=drawer,
                  text=info.surname(),
                  config=coordinates["Surname"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw Given Name
        draw_text(drawer=drawer,
                  text=info.given_name(),
                  config=coordinates["GivenName"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw OEN
        draw_text(drawer=drawer,
                  text=info.OEN(),
                  config=coordinates["OEN"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw student number
        draw_text(drawer=drawer,
                  text=info.student_number(),
                  config=coordinates["StudentNumber"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw gender
        draw_text(drawer=drawer,
                  text=info.gender(),
                  config=coordinates["Gender"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw date of birth year
        draw_text(drawer=drawer,
                  text=info.date_of_birth_y(),
                  config=coordinates["DateOfBirth_Y"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw date of birth month
        draw_text(drawer=drawer,
                  text=info.date_of_birth_m(),
                  config=coordinates["DateOfBirth_M"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw date of birth day
        draw_text(drawer=drawer,
                  text=info.date_of_birth_d(),
                  config=coordinates["DateOfBirth_D"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw name of district school board
        draw_text(drawer=drawer,
                  text=info.name_of_district_school_board(),
                  config=coordinates["NameOfDSB"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw number of district school board
        draw_text(drawer=drawer,
                  text=info.district_school_board_number(),
                  config=coordinates["NumberOfDSB"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw name of school
        draw_text(drawer=drawer,
                  text=info.name_of_school(),
                  config=coordinates["NameOfSchool"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw number of school
        draw_text(drawer=drawer,
                  text=info.school_number(),
                  config=coordinates["NumberOfSchool"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw date of entry year
        draw_text(drawer=drawer,
                  text=info.date_of_entry_y(),
                  config=coordinates["DateOfEntry_Y"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw date of entry month
        draw_text(drawer=drawer,
                  text=info.date_of_entry_m(),
                  config=coordinates["DateOfEntry_M"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw date of entry day
        draw_text(drawer=drawer,
                  text=info.date_of_entry_d(),
                  config=coordinates["DateOfEntry_D"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw specialized program
        draw_text(drawer=drawer,
                  text=info.specialized_program(),
                  config=coordinates["SpecializedProgram"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw diploma or certificate
        draw_text(drawer=drawer,
                  text=info.diploma_or_certificate(),
                  config=coordinates["DiplomaOrCertificate"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw diploma or certificate date year
        draw_text(drawer=drawer,
                  text=info.diploma_or_certificate_date_of_issue_y(),
                  config=coordinates["DiplomaOrCertificate_DateOfIssue_Y"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_center)
        # draw date of birth month
        draw_text(drawer=drawer,
                  text=info.diploma_or_certificate_date_of_issue_m(),
                  config=coordinates["DiplomaOrCertificate_DateOfIssue_M"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_center)
        # draw authorization
        draw_text(drawer=drawer,
                  text=info.authorization(),
                  config=coordinates["Authorization"],
                  font=font,
                  offset=offset,
                  alignment_flag=flag_left)
        # draw community involvement
        if info.community_involvement():
            draw_image(img, checkMark, coordinates["CommunityInvolvement_True"],
                       offset=offset)
        else:
            draw_image(img, checkMark,
                       coordinates["CommunityInvolvement_False"], offset=offset)
        # draw provincial secondary school literacy requirement
        if info.provincial_secondary_school_literacy_requirement():
            draw_image(img, checkMark,
                       coordinates["ProvincialSecondarySchoolLiteracy_True"],
                       offset=offset)
        else:
            draw_image(img, checkMark,
                       coordinates["ProvincialSecondarySchoolLiteracy_False"],
                       offset=offset)
        # save the image
        images.append((img, "{}OST{}.png".format(
            full_name + " " if full_name != "" else "",
            ("_" + str(page_index + 1)) if total_page > 1 else ""),))
    return images, "{}OST".format(full_name + " " if full_name != "" else "")


def draw_text(drawer, text, config, font, offset, alignment_flag=flag_left):
    # get the final position of the text and apply the alignment
    offset_x, offset_y = offset
    box_x, box_y, box_width, box_height, font_size = config
    x = offset_x + box_x
    font = ImageFont.truetype(font, size=font_size) if isinstance(font,
                                                                  str) else font
    # determine how long the text is going to be and apply the alignment flag
    width, height = drawer.textsize(text=text, font=font, spacing=0)
    if alignment_flag is flag_right:
        x = x + box_width - width
    elif alignment_flag is flag_center:
        x = x + box_width / 2 - width / 2
    else:
        x = x
    y = offset_y + box_y + box_height // 2 - height // 2
    # drawer.rectangle(xy=(box_x, box_y, box_x + box_width, box_y + box_height), outline="black", width=1)
    drawer.text(xy=(x, y), text=text, font=font, fill="black")


def draw_image(img, image, config, offset):
    x, y = config
    x += offset[0]
    y += offset[1]
    img.paste(image, (x, y), image)


def draw_courses(courses, font, font_size, spacing):
    # get the info needed to draw courses
    _, _, course_width, course_height = coordinates["Course"]
    date_x, date_width = coordinates["Course_date_offset"]
    level_x, level_width = coordinates["Course_level_offset"]
    title_x, title_width = coordinates["Course_title_offset"]
    code_x, code_width = coordinates["Course_code_offset"]
    percentage_x, percentage_width = coordinates["Course_percentage_offset"]
    credit_x, credit_width = coordinates["Course_credit_offset"]
    compulsory_x, compulsory_width = coordinates["Course_compulsory_offset"]
    note_x, note_width = coordinates["Course_note_offset"]
    font = ImageFont.truetype(font, size=font_size)
    # draw the courses on a new image
    # to make sure there are at least one image
    img = Image.new(mode="RGBA", size=(course_width, course_height),
                    color=(0, 0, 0, 0))
    img_drawer = ImageDraw.Draw(img)
    images = [img]

    def get_height(course):
        # get the maximum height in line
        return max(font.getsize(course.date)[1],
                   font.getsize(course.level)[1],
                   font.getsize(course.title)[1],
                   font.getsize(course.code)[1],
                   font.getsize(course.percentage)[1],
                   font.getsize(course.credit)[1],
                   font.getsize(course.compulsory)[1],
                   font.getsize(course.note)[1],
                   )

    def draw_course(drawer, course: Data.Course, height, y):
        # draw date
        draw_text(drawer=drawer,
                  text=course.date,
                  config=(date_x, y, date_width, height, 0),
                  font=font,
                  offset=(0, 0),
                  alignment_flag=flag_center)
        # draw level
        draw_text(drawer=drawer,
                  text=course.level,
                  config=(level_x, y, level_width, height, 0),
                  font=font,
                  offset=(0, 0),
                  alignment_flag=flag_center)
        # draw title
        draw_text(drawer=drawer,
                  text=course.title,
                  config=(title_x, y, title_width, height, 0),
                  font=font,
                  offset=(0, 0),
                  alignment_flag=flag_left)
        # draw code
        draw_text(drawer=drawer,
                  text=course.code,
                  config=(code_x, y, code_width, height, 0),
                  font=font,
                  offset=(0, 0),
                  alignment_flag=flag_center)
        # draw percentage
        draw_text(drawer=drawer,
                  text=course.percentage,
                  config=(percentage_x, y, percentage_width, height, 0),
                  font=font,
                  offset=(0, 0),
                  alignment_flag=flag_center)
        # draw credit
        draw_text(drawer=drawer,
                  text=course.credit,
                  config=(credit_x, y, credit_width, height, 0),
                  font=font,
                  offset=(0, 0),
                  alignment_flag=flag_center)
        # draw compulsory
        draw_text(drawer=drawer,
                  text=course.compulsory,
                  config=(compulsory_x, y, compulsory_width, height, 0),
                  font=font,
                  offset=(0, 0),
                  alignment_flag=flag_center)
        # draw note
        draw_text(drawer=drawer,
                  text=course.note,
                  config=(note_x, y, note_width, height, 0),
                  font=font,
                  offset=(0, 0),
                  alignment_flag=flag_center)

    accum_y = spacing
    for c in courses:
        # if the height exceed the limit then proceed to next page
        c_height = get_height(c)
        unit_height = c_height + spacing
        if accum_y + unit_height > course_height:
            new_img = Image.new(mode="RGBA", size=(course_width, course_height),
                                color=(0, 0, 0, 0))
            new_img_drawer = ImageDraw.Draw(new_img)
            images.append(new_img)
            img = new_img
            img_drawer = new_img_drawer
            accum_y = spacing
        draw_course(img_drawer, c, c_height, accum_y)
        accum_y += unit_height
    return images