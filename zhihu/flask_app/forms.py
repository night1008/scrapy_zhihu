# coding:utf-8
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, SelectField, SelectMultipleField, HiddenField,BooleanField
from flask import url_for
from flask.helpers import flash
from wtforms.validators import Required, ValidationError, Email, Length, EqualTo

from models.pony_models import User
from pony.orm import db_session, select

class LoginForm(Form):
    email = TextField('邮箱',
                      validators=[Required(message='邮箱不能为空')],
                      description='邮箱')
    password = PasswordField('密码',
                             validators=[Required(message='密码不能为空')],
                             description='密码')

    @db_session
    def validate_email(form, field):
        user = select(u for u in User if u.email == field.data.strip()).first()
        if not user:
            raise ValidationError('邮箱不存在')

    @db_session
    def validate_password(form, field):
        user = select(u for u in User if u.email == form.email.data.strip()).first()
        if not user or not user.check_password(field.data.strip()):
            raise ValidationError('密码不正确')


class SignupForm(Form):
    email = TextField(u'邮箱',
                      validators=[
                            Required(message='邮箱不能为空'), 
                            Email(message='邮箱格式不正确')],
                      description='邮箱')
    password = PasswordField('密码',
                             validators=[
                                    Required(message='密码不能为空'),
                                    Length(min=6, max=30, message='密码最少6位， 最多30位')],
                             description='密码')

    password_confirmation = PasswordField('密码确认',
                                   validators=[
                                        Required(message='确认密码不能为空'),
                                        EqualTo('password', message='密码不一致'),
                                        Length(min=6, max=30, message='密码最少6位， 最多30位')],
                                   description='确认密码')

    @db_session
    def validate_email(form, field):
        user = select(u for u in User if u.email == field.data.strip()).first()
        if user:
            raise ValidationError('邮箱已存在')