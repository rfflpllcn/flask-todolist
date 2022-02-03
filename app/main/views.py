from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.main import main
from app.main.forms import IdeaForm, PortfolioForm
from app.models import Idea, Portfolio, Instrument


@main.route("/")
def index():
    form = IdeaForm()
    if form.validate_on_submit():
        return redirect(url_for("main.new_portfolio"))
    return render_template("index.html", form=form)


@main.route("/portfolios/", methods=["GET", "POST"])
@login_required
def portfolio_overview():
    form = PortfolioForm()
    if form.validate_on_submit():
        return redirect(url_for("main.add_portfolio"))
    return render_template("overview.html", form=form)


def _get_user():
    return current_user.username if current_user.is_authenticated else None


def populate_ideaform_choices(ideaForm):
    instruments = Instrument.query.all()
    isins = [(ins.isin, ins.isin) for ins in instruments]
    ideaForm.isin.choices = isins


@main.route("/portfolio/<int:id>/", methods=["GET", "POST"])
def portfolio(id):
    portfolio = Portfolio.query.filter_by(id=id).first_or_404()
    # print("portfolio ideas", portfolio.ideas)
    form = IdeaForm()
    populate_ideaform_choices(form)
    if form.validate_on_submit():
        print("form.idea.data", form.description.data, form.isin.data)
        instrument = Instrument.query.filter_by(isin=form.isin.data).first_or_404()
        Idea(form.description.data, portfolio.id, instrument.id, _get_user()).save()
        return redirect(url_for("main.portfolio", id=id))
    return render_template("portfolio.html", portfolio=portfolio, form=form)


@main.route("/portfolio/new/", methods=["POST"])
def new_portfolio():
    form = IdeaForm(idea=request.form.get("idea"))
    if form.validate():
        portfolio = Portfolio(creator=_get_user()).save()
        Idea(form.idea.data, portfolio.id).save()
        return redirect(url_for("main.portfolio", id=portfolio.id))
    return redirect(url_for("main.index"))


@main.route("/portfolio/add/", methods=["POST"])
def add_portfolio():
    form = PortfolioForm(idea=request.form.get("title"))
    if form.validate():
        portfolio = Portfolio(form.title.data, _get_user()).save()
        return redirect(url_for("main.portfolio", id=portfolio.id))
    return redirect(url_for("main.index"))
