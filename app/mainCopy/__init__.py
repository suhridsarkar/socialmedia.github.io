from flask import Flask, render_template, request, redirect, session, flash, url_for, Blueprint
from sqlalchemy import and_, or_
from app.models import post, user, postLike,friendrequests, db
from app.commen import greet, generate_id

main_bp = Blueprint("main_bp", __name__)
