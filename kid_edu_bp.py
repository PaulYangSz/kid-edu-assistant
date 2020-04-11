#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 HomeWork Inc. All Rights Reserved.
# Author: shookuooo@gmail.com
import json
import random

import flask as f
from flask import render_template, request

import log

bp = f.Blueprint('kid_edu_v1', __name__)


@bp.route('/math', methods=['POST'])
def get_math_exam():
    grade, cnt = request.form.get('grade'), int(request.form.get('cnt'))
    log.info('\n\n==========\n获取数学{}年级的{}道题目'.format(grade, cnt))
    exams = []
    if grade == 'grade1First':
        for i in range(cnt):
            exam_item = {}
            add_or_subtract = random.randint(1, 2)
            if add_or_subtract == 1:
                a = random.randint(5, 20)
                b = random.randint(3, 20)
                exam_item['itemTitle'] = '{} + {} = '.format(a, b)
                exam_item['itemValue'] = a + b
            else:
                a = random.randint(11, 20)
                b = random.randint(2, a-2)
                exam_item['itemTitle'] = '{} - {} = '.format(a, b)
                exam_item['itemValue'] = a - b
            exams.append(exam_item)
    log.info('题目为:\n{}'.format(exams))
    return json.dumps(exams)


@bp.route('/math/score', methods=['POST'])
def score_math_exam():
    exam_content, duration, answer = request.form.get('examContent'), request.form.get('duration'), request.form.get('answer')
    exam_content = json.loads(exam_content)
    answer = json.loads(answer)
    log.info('@对于题目:\n{}\n@用时:\n{}\n@作答结果\n{}'.format(exam_content, duration, answer))
    corr_cnt = 0
    err_cnt = 0
    for i in range(len(exam_content)):
        try:
            cur_answer = int(answer[i])
        except Exception as e:
            print(e)
            cur_answer = -999
        if cur_answer == exam_content[i]['itemValue']:
            corr_cnt += 1
        else:
            err_cnt += 1
    log.info('@其中作对{}道题，做错{}道题'.format(corr_cnt, err_cnt))
    result_str = '用时: {}\n答对{}道题，答错{}道题'.format(duration, corr_cnt, err_cnt)
    return json.dumps({'duration': duration, 'corrCnt': corr_cnt, 'errCnt': err_cnt, 'result': result_str})


@bp.route('/', methods=['GET'])
def main_page():
    return render_template('kid_edu.html')
