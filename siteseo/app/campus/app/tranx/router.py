from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from typing import List
from siteseo.app.db.session import get_db
from sqlalchemy.orm import Session
from .schema import TranxDto, FeeDto, AccountDto
from . import service
from datetime import date


router = APIRouter(prefix="/tranx", tags=["transactions-mgmt"])


@router.post("/pay")
def make_tranx(tr: TranxDto, db: Session = Depends(get_db)):
    try:
        return service.make_tranx(tr, db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/all")
def all_tranx(db: Session = Depends(get_db)) -> List[TranxDto]:
    """Only Admin."""
    return service.all_tranx(db)


@router.get("/byref")
def tranx_by_ref(ref: str, db: Session = Depends(get_db)) -> TranxDto:
    try:
        return service.tranx_byref(ref, db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/student")
def by_student(sid: str, db: Session = Depends(get_db)) -> List[TranxDto]:
    return service.by_student(sid, db)


@router.get("/range")
def by_range(lower: date, upper: date, db: Session = Depends(get_db)) -> List[TranxDto]:
    """Only admin."""
    return service.by_range(lower, upper, db)


@router.post("fees")
def add_fee(fee: FeeDto, db: Session = Depends(get_db)) -> FeeDto:
    try:
        return service.make_fee(fee, db)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("fees")
def get_fees(db: Session = Depends(get_db)) -> List[FeeDto]:
    return service.all_fees(db)


@router.get("fees/fee")
def get_fee(id: str, db: Session = Depends(get_db)) -> FeeDto:
    return service.get_fee(id, db)


@router.post("/accounts")
def make_account(acct: AccountDto, db: Session = Depends(get_db)) -> AccountDto:
    return service.make_account(acct, db)


@router.get("/accounts")
def all_accounts(db: Session = Depends(get_db)) -> List[AccountDto]:
    return service.all_accounts(db)


@router.get("/accounts/officer")
def account_by_officer(usr: str, db: Session = Depends(get_db)) -> List[AccountDto]:
    return service.accounts_by_officer(usr, db)


@router.post("/fees/upload", status_code=status.HTTP_201_CREATED)
async def upload_fees(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Uploads fee data from a CSV or JSON file.

    Args:
        file (UploadFile): The uploaded file.
        db (Session): The database session object (dependency).

    Returns:
        JSONResponse: Response object containing information about the upload.
    """

    try:
        if file.content_type not in ("text/csv", "application/json"):
            return JSONResponse(
                content={"message": "Invalid file type. Supported types: csv, json"},
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        file_type = file.content_type.split("/")[1]
        uploaded_count = service.bulk_upload_fees(file.filename, file_type, db)

        return JSONResponse(
            content={"message": f"{uploaded_count} fees uploaded successfully."},
            status_code=status.HTTP_201_CREATED,
        )

    except IntegrityError as e:
        print(f"Error uploading fees: {e}")
        return JSONResponse(
            content={"message": "Error uploading fees. Please check the data."},
            status_code=status.HTTP_409_CONFLICT,
        )

    except Exception as e:
        print(f"Unexpected error during upload: {e}")
        return JSONResponse(
            content={"message": "An unexpected error occurred."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
