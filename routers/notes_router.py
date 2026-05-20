from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models import Note, User, NoteShare, NoteVersion
from app.schemas import NoteCreateSchema, ShareSchema

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("", status_code=201)
def create_note(
    data: NoteCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = Note(
        title=data.title,
        content=data.content,
        owner_id=current_user.id
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note

@router.get("")
def get_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    notes = db.query(Note).filter(
        Note.owner_id == current_user.id
    ).all()

    return notes



@router.get("/{note_id}")
def get_single_note(
    note_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.owner_id != current_user.id:

        shared = db.query(NoteShare).filter(
            NoteShare.note_id == note.id,
            NoteShare.shared_with_id == current_user.id
        ).first()

        if not shared:
            raise HTTPException(status_code=403, detail="Access denied")

    return note


@router.put("/{note_id}")
def update_note(
    note_id: str,
    data: NoteCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can update")

    latest_version = db.query(NoteVersion).filter(
        NoteVersion.note_id == note.id
    ).count()

    history = NoteVersion(
        note_id=note.id,
        title=note.title,
        content=note.content,
        version_number=latest_version + 1
    )

    db.add(history)

    note.title = data.title
    note.content = data.content

    db.commit()
    db.refresh(note)

    return note




@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can delete")

    db.delete(note)
    db.commit()



@router.post("/{note_id}/share")
def share_note(
    note_id: str,
    data: ShareSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner can share")

    target_user = db.query(User).filter(
        User.email == data.share_with_email
    ).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")

    existing_share = db.query(NoteShare).filter(
        NoteShare.note_id == note.id,
        NoteShare.shared_with_id == target_user.id
    ).first()

    if existing_share:
        raise HTTPException(status_code=400, detail="Already shared")

    share = NoteShare(
        note_id=note.id,
        shared_with_id=target_user.id
    )

    db.add(share)
    db.commit()

    return {
        "message": "Note shared successfully"
    }


@router.get("/{note_id}/history")
def get_note_history(
    note_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only owner allowed")

    versions = db.query(NoteVersion).filter(
        NoteVersion.note_id == note.id
    ).all()

    return versions