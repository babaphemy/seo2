from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
import csv
import json
from sqlalchemy.exc import IntegrityError
from .schema import TranxDto, FeeDto, AccountDto
from .models import Tranx, Fee, Account
from siteseo.app.campus.app.classroom.models import Classroom
from siteseo.app.campus.app.info.models import Appuser
from espy_contact.util.enums import StatusEnum
import datetime


def make_tranx(tr: TranxDto, db: Session) -> bool:
    try:
        owner = db.query(Appuser).get(tr.payee_id)
        if not owner:
            raise ValueError(f"No user with ID: {tr.payee_id}")
        new_tranx = Tranx(**tr.__dict__)
        db.add(new_tranx)
        db.commit()
        db.refresh
        tr.id = new_tranx.id
        return tr
    except Exception as e:
        raise e


def all_tranx(db: Session) -> List[TranxDto]:
    return db.query(Tranx).all()


def tranx_byref(ref: str, db: Session) -> TranxDto:
    try:
        tr = db.query(Tranx).filter(Tranx.ref == ref).first()
        if not tr:
            raise ValueError(f"No Tranx with ref provided {ref}")
        return tr
    except Exception as e:
        raise e


def by_student(sid: str, db: Session) -> List[TranxDto]:
    """
    This function retrieves all transactions for a specific student ID.

    Args:
        sid (str): The student ID to filter by.
        db (Session): The database session object.

    Returns:
        List[TranxDto]: A list of TranxDto objects for the student's transactions.
    """
    transactions = db.query(Tranx).filter(Tranx.payee_id == sid).all()
    return transactions


def by_range(lower: date, upper: date, db: Session) -> List[TranxDto]:
    """
    This function retrieves all transactions within a date range.

    Args:
        lower (date): The lower bound of the date range (inclusive).
        upper (date): The upper bound of the date range (inclusive).
        db (Session): The database session object.

    Returns:
        List[TranxDto]: A list of TranxDto objects for transactions within the range.
    """
    transactions = (
        db.query(Tranx).filter(Tranx.date >= lower, Tranx.date <= upper).all()
    )
    return transactions


def edit_tranx(ref: str, data: dict, db: Session) -> TranxDto:
    """
    This function edits a transaction based on its reference number.

    Args:
        ref (str): The reference number of the transaction to edit.
        data (dict): A dictionary containing the updated values for the transaction.
        db (Session): The database session object.

    Returns:
        TranxDto: The updated TranxDto object representing the edited transaction.

    Raises:
        ValueError: If no transaction is found with the provided reference number.
    """

    try:
        # Get the transaction to edit
        transaction = db.query(Tranx).filter(Tranx.ref == ref).first()
        if not transaction:
            raise ValueError(f"No Tranx with ref provided {ref}")

        # Update the transaction object with new data
        for key, value in data.items():
            if hasattr(transaction, key):  # Check if attribute exists
                setattr(transaction, key, value)

        # Commit the changes to the database
        db.commit()

        # Return the updated transaction object
        return transaction

    except Exception as e:
        # Rollback any changes if an error occurs
        db.rollback()
        raise e


def make_fee(fee: FeeDto, db: Session) -> FeeDto:
    try:
        # a classroom called ALL must exist for fees assigned to all students
        cid = fee.classroom_id
        fee_class = db.query(Fee).filter(Fee.classroom_id == cid)
        if not fee_class:
            raise ValueError(f"No Classroom with ID {cid}")

        new_fee = Fee(
            classroom_id=cid,
            name=fee.fee_name,
            amount=fee.amount,
            due_date=fee.due_date,
            start_date=fee.start_date,
            status=fee.status,
            classroom=fee_class,
        )
        db.add(new_fee)
        db.commit()
        db.refresh(new_fee)
    except Exception as e:
        raise e


def all_fees(db: Session) -> List[FeeDto]:
    return db.query(Fee).all()


def get_fee(id: str, db: Session) -> Optional[FeeDto]:
    return db.query(Fee).get(id)


def fee_class(cid: str, db: Session) -> List[FeeDto]:
    try:
        cl = db.query(Classroom).get(cid)
        if not cl:
            raise ValueError(f"No Classroom with ID {cid}")
        fees = db.query(Fee).filter(Fee.classroom_id == cid).all()
        return fees
    except Exception as e:
        raise e


def edit_fee():
    pass


def make_account(account: AccountDto, db: Session) -> AccountDto:
    try:
        new_acct = Account(
            bank=account.bank,
            account_name=account.account_name,
            account_number=account.account_number,
            currency=account.currency,
            is_active=account.is_active,
            account_officer=account.account_officer,
            account_admin=account.account_admin,
            created_on=account.created,
            modified_on=account.modified,
        )
        db.add(new_acct)
        db.refresh(new_acct)
        pass
    except Exception as e:
        raise e


def all_accounts(db: Session) -> List[AccountDto]:
    return db.query(Account).all()


def accounts_by_officer(usr: str, db: Session) -> List[AccountDto]:
    return db.query(Account).filter(Account.account_admin == usr)


def edit_account():
    pass


def bulk_upload_fees(file_path: str, file_type: str, db: Session) -> int:
    """
    Uploads fee data from a CSV or JSON file.

    Args:
        file_path (str): The path to the CSV or JSON file.
        file_type (str): "csv" or "json".
        db (Session): The database session object.

    Returns:
        int: The number of fees successfully uploaded.
    """

    uploaded_count = 0
    with open(file_path, "r") as file:
        if file_type == "csv":
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Convert string date to datetime objects
                    due_date = datetime.strptime(row["due_date"], "%Y-%m-%d").date()
                    start_date = datetime.strptime(row["start_date"], "%Y-%m-%d").date()
                    fee = Fee(
                        classroom_id=row["classroom_id"],
                        name=row["name"],
                        amount=float(row["amount"]),
                        due_date=due_date,
                        start_date=start_date,
                        status=StatusEnum[
                            row["status"]
                        ],  # Assuming 'status' is stored as an enum string
                    )
                    uploaded_count += 1
                    db.add(fee)
                    db.commit()
                except IntegrityError as e:
                    db.rollback()
                    print(f"Error uploading fee (row {reader.line_no}): {e}")
                except Exception as e:
                    print(f"Error processing fee data (row {reader.line_no}): {e}")

        elif file_type == "json":
            data = json.load(file)
            for fee_data in data:
                try:
                    due_date = datetime.strptime(
                        fee_data["due_date"], "%Y-%m-%d"
                    ).date()
                    start_date = datetime.strptime(
                        fee_data["start_date"], "%Y-%m-%d"
                    ).date()
                    fee = Fee(
                        classroom_id=fee_data["classroom_id"],
                        name=fee_data["name"],
                        amount=float(fee_data["amount"]),
                        due_date=due_date,
                        start_date=start_date,
                        status=StatusEnum[
                            fee_data["status"]
                        ],  # Assuming 'status' is stored as an enum string
                    )
                    uploaded_count += 1
                    db.add(fee)
                    db.commit()
                except IntegrityError as e:
                    db.rollback()
                    print(f"Error uploading fee (index {data.index(fee_data)}): {e}")
                except Exception as e:
                    print(
                        f"Error processing fee data (index {data.index(fee_data)}): {e}"
                    )
        else:
            raise ValueError("Invalid file type. Supported types: csv, json")

    return uploaded_count


def debtors_list(db: Session):
    pass
