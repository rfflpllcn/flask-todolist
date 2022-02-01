from flask import abort, request, url_for, jsonify

from app.api import api
from app.decorators import admin_required
from app.models import Idea, Portfolio, User


@api.route("/")
def get_routes():
    return {
        "users": url_for("api.get_users", _external=True),
        "portfolios": url_for("api.get_portfolios", _external=True),
    }


@api.route("/users/")
def get_users():
    return {"users": [user.to_dict() for user in User.query.all()]}


@api.route("/user/<string:username>/")
def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return user.to_dict()


@api.route("/user/", methods=["POST"])
def add_user():
    try:
        user = User(
            username=request.json.get("username"),
            email=request.json.get("email"),
            password=request.json.get("password"),
        ).save()
    except:
        abort(400)
    return user.to_dict(), 201


@api.route("/user/<string:username>/portfolios/")
def get_user_portfolios(username):
    user = User.query.filter_by(username=username).first_or_404()
    portfolios = user.portfolios
    return {"portfolios": [portfolio.to_dict() for portfolio in portfolios]}


@api.route("/user/<string:username>/portfolio/<int:portfolio_id>/")
def get_user_portfolio(username, portfolio_id):
    user = User.query.filter_by(username=username).first()
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if not user or username != portfolio.creator:
        abort(404)
    return portfolio.to_dict()


@api.route("/user/<string:username>/portfolio/", methods=["POST"])
def add_user_portfolio(username):
    user = User.query.filter_by(username=username).first_or_404()
    try:
        portfolio = Portfolio(
            title=request.json.get("title"), creator=user.username
        ).save()
    except:
        abort(400)
    return portfolio.to_dict(), 201


@api.route("/portfolios/")
def get_portfolios():
    portfolios = Portfolio.query.all()
    return {"portfolios": [portfolio.to_dict() for portfolio in portfolios]}


@api.route("/portfolio/<portfolio_id>/")
def get_portfolio(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    return portfolio.to_dict()


@api.route("/portfolio/", methods=["POST"])
def add_portfolio():
    try:
        portfolio = Portfolio(title=request.json.get("title")).save()
    except:
        abort(400)
    return portfolio.to_dict(), 201


@api.route("/portfolio/<int:portfolio_id>/ideas/")
def get_portfolio_ideas(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    return {"ideas": [idea.to_dict() for idea in portfolio.ideas]}


@api.route("/user/<string:username>/portfolio/<int:portfolio_id>/ideas/")
def get_user_portfolio_ideas(username, portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if portfolio.creator != username:
        abort(404)
    return {"ideas": [idea.to_dict() for idea in portfolio.ideas]}


@api.route("/user/<string:username>/portfolio/<int:portfolio_id>/", methods=["POST"])
def add_user_portfolio_idea(username, portfolio_id):
    user = User.query.filter_by(username=username).first_or_404()
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    try:
        idea = Idea(
            description=request.json.get("description"),
            portfolio_id=portfolio.id,
            creator=user.username,
        ).save()
    except:
        abort(400)
    return idea.to_dict(), 201


@api.route("/portfolio/<int:portfolio_id>/", methods=["POST"])
def add_portfolio_idea(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    try:
        idea = Idea(
            description=request.json.get("description"), portfolio_id=portfolio.id
        ).save()
    except:
        abort(400)
    return idea.to_dict(), 201


@api.route("/idea/<int:idea_id>/")
def get_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    return idea.to_dict()


@api.route("/idea/<int:idea_id>/", methods=["PUT"])
def update_idea_status(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    try:
        if request.json.get("is_finished"):
            idea.finished()
        else:
            idea.reopen()
    except:
        abort(400)
    return idea.to_dict()


@api.route("/portfolio/<int:portfolio_id>/", methods=["PUT"])
def change_portfolio_title(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    try:
        portfolio.title = request.json.get("title")
        portfolio.save()
    except:
        abort(400)
    return portfolio.to_dict()


@api.route("/user/<string:username>/", methods=["DELETE"])
@admin_required
def delete_user(username):
    user = User.query.get_or_404(username=username)
    try:
        if username == request.json.get("username"):
            user.delete()
            return {}
        else:
            abort(400)
    except:
        abort(400)


@api.route("/portfolio/<int:portfolio_id>/", methods=["DELETE"])
@admin_required
def delete_portfolio(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    try:
        if portfolio_id == request.json.get("portfolio_id"):
            portfolio.delete()
            return jsonify()
        else:
            abort(400)
    except:
        abort(400)


@api.route("/idea/<int:idea_id>/", methods=["DELETE"])
@admin_required
def delete_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    try:
        if idea_id == request.json.get("idea_id"):
            idea.delete()
            return jsonify()
        else:
            abort(400)
    except:
        abort(400)
