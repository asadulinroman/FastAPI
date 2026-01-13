from pydantic import BaseModel


class AnalyzeDocShema(BaseModel):
    filename: str

class SendMessageToEmailSchema(BaseModel):
    email: str
    extracted_text: str