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


def add_difficulty_match(difficulty, first, second):
    if difficulty == 1:
        return True
    elif difficulty == 2:
        if first % 10 + second % 10 >= 10:
            return True
        else:
            return False
    elif difficulty == 3:
        if first % 10 + second % 10 >= 10 and first//10 % 10 + second//10 % 10 >= 9:
            return True
        else:
            return False


def subtract_difficulty_match(difficulty, first, second):
    if difficulty == 1:
        return True
    elif difficulty == 2:
        if first % 10 < second % 10:
            return True
        else:
            return False
    elif difficulty == 3:
        if first % 10 < second % 10 and first//10 % 10 <= second//10 % 10:
            return True
        else:
            return False


@bp.route('/math', methods=['POST'])
def get_math_exam():
    grade, difficulty, cnt = request.form.get('grade'), request.form.get('difficulty'), int(request.form.get('cnt'))
    difficulty = int(difficulty)
    log.info('\n\n==========\n获取数学 {}年级 难度{} 的{}道题目'.format(grade, difficulty, cnt))
    exams = []
    max_iter_n = 1000
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
    elif grade == 'grade2Second':
        for i in range(cnt):
            exam_item = {}
            add_or_subtract = random.randint(1, 2)
            if add_or_subtract == 1:
                a = random.randint(300, 899)
                max_remain = 1000 - a
                b = random.randint(20, max_remain)
                iter_i = 0
                while not add_difficulty_match(difficulty, a, b):
                    a = random.randint(300, 899)
                    max_remain = 1000 - a
                    b = random.randint(20, max_remain)
                    if iter_i > max_iter_n:
                        break
                    else:
                        iter_i += 1
                exam_item['itemTitle'] = '{} + {} = '.format(a, b)
                exam_item['itemValue'] = a + b
            else:
                a = random.randint(201, 999)
                b = random.randint(100, a-2)
                iter_i = 0
                while not subtract_difficulty_match(difficulty, a, b):
                    a = random.randint(201, 999)
                    b = random.randint(100, a - 2)
                    if iter_i > max_iter_n:
                        break
                    else:
                        iter_i += 1
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
    if err_cnt == 0:
        result_str = '用时: {}\n答对{}道题，答错{}道题\n(*@ο@*) 哇～ 全做对了！荣耀归主！'.format(duration, corr_cnt, err_cnt)
    else:
        result_str = '用时: {}\n答对{}道题，答错{}道题'.format(duration, corr_cnt, err_cnt)
    return json.dumps({'duration': duration, 'corrCnt': corr_cnt, 'errCnt': err_cnt, 'result': result_str})


@bp.route('/', methods=['GET'])
def main_page():
    return render_template('kid_edu.html')
