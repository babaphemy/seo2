from fastapi import APIRouter, Depends, HTTPException, status,Request
from .schema import MailerDto
from . import service
from .models import Message
from .schema import Message as MsgDto
from .listener import message_queue
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse
from sqlalchemy.orm import Session
from sse_starlette import sse
from siteseo.app.db.session import get_db

router = APIRouter(prefix="/messaging", tags=["notifications"])

async def event_stream(request: Request):
    while True:
        message = await message_queue.get()
        yield f"data: {message}\n\n"


@router.post("/emails/bulk", status_code=status.HTTP_202_ACCEPTED)
async def send_bulk_emails(mailer: MailerDto, db: Session = Depends(get_db)):
    """
    Sends a bulk email to the specified list of recipients.

    Args:
        recipients (List[str]): A list of email addresses to send the email to.

    Returns:
        JSONResponse: A JSON response indicating the success or failure of the operation.
    """

    try:
        success = service.send_bulk_email(mailer, db)
        if success:
            return JSONResponse(
                content={"message": "Emails sent successfully."},
                status_code=status.HTTP_202_ACCEPTED,
            )
        else:
            return JSONResponse(
                content={"message": "Failed to send emails."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/emails/local", status_code=status.HTTP_202_ACCEPTED)
async def send_emails(mailer: MailerDto) -> bool:
    """
    Sends an email to a list of recipients.

    Args:
        mailer (MailerDto): A DTO containing email details.

    Returns:
        JSONResponse: A JSON or boolean response indicating the success or failure of the operation.
    """

    try:
        success = service.send_email(mailer)
        if success:
            return JSONResponse(
                content={"message": "Emails sent successfully."},
                status_code=status.HTTP_202_ACCEPTED,
            )
        else:
            return JSONResponse(
                content={"message": "Failed to send some or all emails."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
@router.post("/messages")
async def create_message(message: MsgDto, db: Session = Depends(get_db)):
    """create new in-app messages."""
    service.send_inapp(db, message)
    return {"message": "Message created successfully"}

@router.get("/stream", response_class=StreamingResponse)
async def stream(request: Request):
    """Stream in-app messages to any UI."""
    return StreamingResponse(event_stream(request), media_type="text/event-stream")
