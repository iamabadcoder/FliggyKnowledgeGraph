# coding:utf-8
import os
import re
from collections import OrderedDict

from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag

import util


def page_cmp(a, b):
    mid = cssBox['w0']['width'] / 2
    if (a['left'] < mid and b['left'] < mid) or (a['left'] > mid and b['left'] > mid):
        return int(a['left'] - b['left']) if abs(int(b['bottom'] - a['bottom'])) <= 5 \
            else int(b['bottom'] - a['bottom'])  # ignore decimal， roughly compare
    else:
        return int(a['left'] - b['left'])


def hearder_footer_filter(element):
    footer = 0.05 * cssBox['h0']['height']
    return element.has_key('bottom') and element['bottom'] > footer


def get_contents(eachPage_html):
    # fetch_all
    element_list = []
    for eachEle in list(eachPage_html.children):
        if ''.join(eachEle.stripped_strings).find(u'小贴士') >= 0:
            continue
        element = {}
        element.setdefault('zzz', eachEle)
        if isinstance(eachEle, Tag):
            for cls in eachEle['class']:
                if cls in cssBox:
                    for i, j in cssBox[cls].items():
                        element.setdefault(i, j)
        # filter
        if hearder_footer_filter(element):
            element_list.append(element)
    # sort
    element_list = sorted(element_list, cmp=page_cmp)

    _element_list = []
    for i in element_list:
        _element_list.append(i['zzz'])
    return tuple(_element_list)


def isbanner(element_html):
    rule_1 = isinstance(element_html, Tag) and element_html.name == 'div' and 'c' in element_html['class'][0]
    if not rule_1: return -1

    first_generation = element_html.contents
    rule_2 = (first_generation is not None) and len(first_generation) == 1 and \
             isinstance(first_generation[0], Tag) and \
             first_generation[0].name == 'div' and 't' in first_generation[0]['class'][0]
    if not rule_2: return -2

    second_generation = first_generation[0].contents
    rule_3 = (second_generation is not None) and len(second_generation) >= 2 and \
             isinstance(second_generation[-2], Tag) and second_generation[-2].name == 'span' and \
             '_' in second_generation[-2]['class'] and ''.join(second_generation[-2].contents).strip() == '' and \
             isinstance(second_generation[-1], Tag) and second_generation[-1].name == 'span'
    if not rule_3: return -3

    third_generation = second_generation[-1].contents
    rule_4 = (third_generation is not None) and len(third_generation) >= 2 and \
             isinstance(third_generation[0], NavigableString) and \
             isinstance(third_generation[-1], Tag) and third_generation[-1].name == 'span' and \
             len(third_generation[-1].contents) == 1 and third_generation[-1].contents[0].strip() == ''
    if not rule_4: return -4
    return 1


def joint(section):
    joint_section = []
    unit = []
    for idx in range(len(section)):
        big_element = section[idx]

        if len(unit) > 0 and isinstance(big_element, Tag) and 'c' in big_element['class'] and ''.join(
                big_element.stripped_strings).strip() is not '':
            joint_section.append(tuple(unit))
            unit = []
        elif 'c' in section[idx - 1]['class'] and len(unit) > 0:
            joint_section.append(tuple(unit))
            unit = []
            # elif 't' in big_element['class'] and idx > 0 and 'c' in section[idx - 1]['class'] \
            #         and re.compile(u'^[0-9１２３４５６７８９０]+$').match(''.join(section[idx - 1].stripped_strings).strip(' ')):
            # print big_element
            # unit.append(big_element)
            # continue

        text_list = [big_element] if isinstance(big_element, Tag) and 't' in big_element['class'] \
            else big_element.find_all(class_='t')
        for element in text_list:
            unit.append(element)
            # if isinstance(element, Tag) and 'c' in element['class'] and ''.join(element.stripped_strings).strip() is not '':
            #     joint_section.append(tuple(unit))
            #     unit = []
            #     continue
            for i in element.descendants:
                rule_new_line = isinstance(i, Tag) and i.name == 'span' and ('_' not in i['class']) and \
                                len(i.contents) == 1 and i.contents[0] == ' '
                if rule_new_line:
                    joint_section.append(tuple(unit))
                    unit = []
                    # print i, element
                    break
    if len(unit) > 0:
        joint_section.append(tuple(unit))
    return tuple(joint_section)


def get_element_list(allPages):
    element_list = []
    for i in list(allPages.find_all('div', class_=re.compile('^pc'))):
        onePage = get_contents(i)
        element_list.extend(onePage)
    return tuple(element_list)


def get_sections(element_list):
    all_sections = []
    section = []
    for i in element_list:
        if isbanner(i) > 0:
            all_sections.append(section)
            section = []
        section.append(i)
    if len(section) > 0:
        all_sections.append(section)
    return tuple(all_sections)


def title_cmp(a, b):
    # todo: campare a,b according to css
    if cssBox[a[0][0]]['font-size'] == cssBox[b[0][0]]['font-size']:
        return len(a[1][0]) - len(b[1][0]) if abs(a[1][1] - b[1][1]) < 5 else a[1][1] - b[1][1]
    else:
        return int(cssBox[b[0][0]]['font-size'] - cssBox[a[0][0]]['font-size'])


def count_fsfcff(section_joint):
    fsfcff_count = {}
    for unit in section_joint[1:]:
        fsfcff_lentext = {}
        for each_element in unit:
            if not isinstance(each_element, Tag):
                continue
            for text_node in each_element.strings:
                if len(text_node.strip()) == 0: continue
                if re.compile(u'[\u4e00-\u9fa5]+').search(text_node.strip()) is None:
                    continue
                _fs = -1
                _fc = -1
                _ff = -1
                for text_parent in text_node.parents:
                    if _fs is not -1 and _fc is not -1 and _ff is not -1:
                        break
                    if isinstance(text_parent, Tag) and (text_parent.name == 'div' or text_parent.name == 'span'):
                        for cls in text_parent['class']:
                            if _fs == -1 and cls.startswith('fs'):
                                _fs = cls
                            elif _fc == -1 and cls.startswith('fc'):
                                _fc = cls
                            elif _ff == -1 and cls.startswith('ff'):
                                _ff = cls
                # print text_node, (_fs, _fc, _ff)
                fsfcff_lentext.setdefault((_fs, _fc, _ff), 0)
                fsfcff_lentext[(_fs, _fc, _ff)] += len(text_node)
        if len(fsfcff_lentext) == 0:
            continue
        fsfcff_longest_text = sorted(fsfcff_lentext.items(), key=lambda x: x[1], reverse=True)[0]
        fsfcff_count.setdefault(fsfcff_longest_text[0], [set(), 0])
        fsfcff_count[fsfcff_longest_text[0]][0].add(unit)
        fsfcff_count[fsfcff_longest_text[0]][1] += fsfcff_longest_text[1]

    fsfcff_count = OrderedDict(sorted(fsfcff_count.items(), cmp=title_cmp))
    # print ''.join(section_joint[0][0].stripped_strings)
    # for i, j in fsfcff_count.items():
    #     print i, len(j[0]), j[1]
    # print '\n\n'
    return fsfcff_count


if __name__ == '__main__':
    global cssBox
    path = 'ctrip_html/'
    out_path = 'ctrip_md/'
    for html_doc in os.listdir(path):
        print html_doc
        # a = 'n'
        # while a[0] is not 'y':
        #     a = raw_input("execute?")
        whole = BeautifulSoup(open(os.path.join(path, html_doc)), 'html.parser')
        container = whole.find('div', attrs={'id': 'page-container'})
        css = ''.join(whole.find_all('style')[2].stripped_strings)
        cssBox = util.get_css_box(css)
        element_list = get_element_list(whole)
        # for i in element_list:
        #     print i

        all_sections = get_sections(element_list)

        # print section name
        # for sec in all_sections:
        #     print ''.join(sec[0].stripped_strings)
        # print '\n\n\n\n\n'

        all_section_joint = []
        for sec in all_sections:
            all_section_joint.append(joint(sec))

        # for sec in all_section_joint:
        #     for u in sec:
        #         for k in u:
        #             print ''.join(k.stripped_strings),
        #         print
        #     print
        #     print

        f = open(os.path.join(out_path, html_doc) + '.md', 'w')

        for section in all_section_joint:
            font_count = count_fsfcff(section)

            # for i, j in font_count.items():
            #     print i
            #     for k in j[0]:
            #         for x in k:
            #             print ''.join(x.stripped_strings),
            #     print
            #     print
            # print '---------------------section---------------------'

            idx = 2
            grade = {}
            for font, count in font_count.items():
                for unit in count[0]:
                    grade.setdefault(unit, idx)
                idx += 1

            flush = []
            f.write('# ' + ''.join(section[0][0].stripped_strings).encode('utf-8') + '\n')
            for unit in section[1:]:
                if not grade.has_key(unit):
                    flush.append(unit)
                    continue
                gd = '#' * grade[unit] + ' '
                f.write(gd)
                if len(flush) > 0:
                    for u in flush:
                        for element in u:
                            f.write(''.join(element.stripped_strings).encode('utf-8'))
                    flush = []
                for element in unit:
                    f.write(''.join(element.stripped_strings).encode('utf-8'))
                f.write('\n')

        f.close()
