
from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas
from .auth import get_password_hash
from typing import List, Optional


# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
#def get_user(db:Session, user_id:int)

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "password":
            value = get_password_hash(value)
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# Project CRUD operations
def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100, owner_id: Optional[int] = None):
    query = db.query(models.Project)
    if owner_id:
        query = query.filter(models.Project.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.ProjectCreate, owner_id: int):
    db_project = models.Project(**project.dict(), owner_id=owner_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project_update: schemas.ProjectUpdate):
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project


# Feature Flag CRUD operations
def get_feature_flag(db: Session, flag_id: int):
    return db.query(models.FeatureFlag).filter(models.FeatureFlag.id == flag_id).first()


def get_feature_flags(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    project_id: Optional[int] = None,
    environment: Optional[models.Environment] = None
):
    query = db.query(models.FeatureFlag)
    if project_id:
        query = query.filter(models.FeatureFlag.project_id == project_id)
    if environment:
        query = query.filter(models.FeatureFlag.environment == environment)
    return query.offset(skip).limit(limit).all()


def create_feature_flag(db: Session, flag: schemas.FeatureFlagCreate, created_by_id: int):
    db_flag = models.FeatureFlag(**flag.dict(), created_by_id=created_by_id)
    db.add(db_flag)
    db.commit()
    db.refresh(db_flag)
    return db_flag


def update_feature_flag(db: Session, flag_id: int, flag_update: schemas.FeatureFlagUpdate):
    db_flag = get_feature_flag(db, flag_id)
    if not db_flag:
        return None
    
    update_data = flag_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_flag, field, value)
    
    db.commit()
    db.refresh(db_flag)
    return db_flag


def delete_feature_flag(db: Session, flag_id: int):
    db_flag = get_feature_flag(db, flag_id)
    if db_flag:
        db.delete(db_flag)
        db.commit()
    return db_flag


def get_feature_flag_by_name_and_project(db: Session, name: str, project_id: int):
    return db.query(models.FeatureFlag).filter(
        and_(
            models.FeatureFlag.name == name,
            models.FeatureFlag.project_id == project_id
        )
    ).first() 
