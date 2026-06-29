"""
Gerenciador de Atividades (classe ``ActivityManager`` do diagrama de classes).

Concentra as regras de negócio de atividades e matrículas: controle de vagas,
entrada em lista de espera, permissões e geração de relatórios. Delega toda a
persistência aos repositórios — não escreve SQL.
"""

from __future__ import annotations

from elder_app.models import Activity, ActivityReport, EnrollmentStatus, User
from elder_app.repositories import ActivityRepository, EnrollmentRepository


class ActivityManager:
    def __init__(
        self, activities: ActivityRepository, enrollments: EnrollmentRepository
    ) -> None:
        self._activities = activities
        self._enrollments = enrollments

    # --- Consultas -------------------------------------------------------
    def get_available_activities(self) -> list[Activity]:
        return self._activities.list_all()

    def get_activity(self, activity_id: int) -> Activity | None:
        return self._activities.get_by_id(activity_id)

    def get_enrollment_status(
        self, senior_id: int, activity_id: int
    ) -> EnrollmentStatus | None:
        return self._enrollments.get_status(senior_id, activity_id)

    # --- Ações do Sênior -------------------------------------------------
    def enroll(self, senior: User, activity: Activity) -> bool:
        """Matricula o Sênior se houver vaga; consome uma vaga da atividade."""
        if not activity.has_open_spots:
            return False
        if self._enrollments.get_status(senior.id, activity.id) is not None:
            return False
        self._enrollments.create(senior.id, activity.id, "enrolled")
        self._activities.update_remaining_spots(
            activity.id, activity.remaining_spots - 1
        )
        return True

    def add_to_queue(self, senior: User, activity: Activity) -> bool:
        """Coloca o Sênior na lista de espera (não consome vaga)."""
        if self._enrollments.get_status(senior.id, activity.id) is not None:
            return False
        self._enrollments.create(senior.id, activity.id, "waitlist")
        return True

    def cancel_enrollment(self, senior: User, activity: Activity) -> None:
        """Desfaz matrícula/lista de espera, devolvendo a vaga se aplicável."""
        status = self._enrollments.get_status(senior.id, activity.id)
        if status is None:
            return
        self._enrollments.delete(senior.id, activity.id)
        if status == "enrolled":
            self._activities.update_remaining_spots(
                activity.id, activity.remaining_spots + 1
            )

    # --- Ações do Tutor (UC11/UC21) -------------------------------------
    def register_new_activity(
        self,
        tutor: User,
        *,
        title: str,
        type: str,
        time: str,
        location: str,
        total_spots: int,
        emoji: str,
        color: str,
        description: str,
    ) -> Activity | None:
        """Publica uma nova atividade. Restrito a tutores (controle de acesso)."""
        if not tutor.is_tutor:
            return None
        activity = Activity(
            id=0,
            title=title,
            tutor_name=tutor.name,
            time=time,
            location=location,
            type=type,
            total_spots=total_spots,
            remaining_spots=total_spots,
            emoji=emoji,
            color=color,
            description=description,
        )
        return self._activities.insert(activity)

    def delete_activity(self, tutor: User, activity_id: int) -> bool:
        if not tutor.is_tutor:
            return False
        self._activities.delete(activity_id)
        return True

    def make_activity_report(self, activity: Activity) -> ActivityReport:
        return ActivityReport(
            activity=activity,
            enrolled_count=self._enrollments.count_by_status(activity.id, "enrolled"),
            waitlist_count=self._enrollments.count_by_status(activity.id, "waitlist"),
        )
