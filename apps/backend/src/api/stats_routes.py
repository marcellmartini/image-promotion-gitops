# pylint: disable=not-callable
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from adapters import get_db
from adapters.database.models import UserModel

from .auth_routes import require_admin
from .schemas import StatsResponse, UserResponse, UserRoleEnum

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get(
    "",
    response_model=StatsResponse,
    summary="Estatísticas",
    description="Retorna estatísticas do sistema. Requer permissão de admin.",
)
def get_stats(
    _current_user: UserResponse = Depends(require_admin),
    db: Session = Depends(get_db),
) -> StatsResponse:
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())
    month_start = today_start.replace(day=1)

    # Total de usuários
    total_users = db.query(func.count(UserModel.id)).scalar() or 0

    # Usuários criados hoje
    users_today = (
        db.query(func.count(UserModel.id))
        .filter(UserModel.created_at >= today_start)
        .scalar()
        or 0
    )

    # Usuários criados esta semana
    users_this_week = (
        db.query(func.count(UserModel.id))
        .filter(UserModel.created_at >= week_start)
        .scalar()
        or 0
    )

    # Usuários criados este mês
    users_this_month = (
        db.query(func.count(UserModel.id))
        .filter(UserModel.created_at >= month_start)
        .scalar()
        or 0
    )

    # Últimos 5 usuários cadastrados
    recent_users_models = (
        db.query(UserModel)
        .order_by(UserModel.created_at.desc())
        .limit(5)
        .all()
    )
    recent_users = [
        UserResponse(
            id=u.id,
            name=u.name,
            email=u.email,
            role=UserRoleEnum(u.role),
            created_at=u.created_at,
            updated_at=u.updated_at,
        )
        for u in recent_users_models
    ]

    # Dados de crescimento (últimos 30 dias)
    growth_data = []
    for i in range(30, -1, -1):
        day = today_start - timedelta(days=i)
        day_end = day + timedelta(days=1)
        count = (
            db.query(func.count(UserModel.id))
            .filter(UserModel.created_at >= day)
            .filter(UserModel.created_at < day_end)
            .scalar()
            or 0
        )
        growth_data.append({
            "date": day.strftime("%Y-%m-%d"),
            "count": count,
        })

    return StatsResponse(
        total_users=total_users,
        users_today=users_today,
        users_this_week=users_this_week,
        users_this_month=users_this_month,
        recent_users=recent_users,
        growth_data=growth_data,
    )
