from app.api.base.controller import BaseController
from app.api.v1.endpoints.repository import repos_get_data_model_config
from app.third_parties.oracle.models.master_data.e_banking import (
    EBankingNotification, EBankingQuestion
)


class CtrConfigEBanking(BaseController):
    async def ctr_e_banking_notification_info(self):
        e_banking_notification_info = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session, model=EBankingNotification
            )
        )
        return self.response(e_banking_notification_info)

    async def ctr_e_banking_question_info(self, e_banking_question_type: str):
        e_banking_question_infos = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session, model=EBankingQuestion,
                is_special_dropdown=True
            )
        )

        questions = []

        for e_banking_question_info in e_banking_question_infos:
            if e_banking_question_info['type'] == e_banking_question_type:
                questions.append(e_banking_question_info)

        return self.response(questions)

    async def ctr_e_banking_question_type_info(self):
        e_banking_question_type_infos = self.call_repos(
            await repos_get_data_model_config(
                session=self.oracle_session, model=EBankingQuestion,
                is_special_dropdown=True
            )
        )
        data = []
        previous_type = None
        for e_banking_question_type_info in e_banking_question_type_infos:
            if e_banking_question_type_info == e_banking_question_type_infos[0]:
                previous_type = e_banking_question_type_info['type']
                data.append(e_banking_question_type_info)
            if e_banking_question_type_info['type'] != previous_type:
                data.append(e_banking_question_type_info)
                previous_type = e_banking_question_type_info['type']

        return self.response(data=data)
