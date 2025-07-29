from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import get_current_active_user
from ..crud import get_projects, get_project, create_project, update_project, delete_project
from ..schemas import Project, ProjectCreate, ProjectUpdate
from ..models import User as UserModel

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=List[Project])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Users can only see their own projects unless they're admin
    if current_user.role == "admin":
        projects = get_projects(db, skip=skip, limit=limit)
    else:
        projects = get_projects(db, skip=skip, limit=limit, owner_id=current_user.id)
    return projects


@router.post("/", response_model=Project)
def create_new_project(
    project: ProjectCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return create_project(db=db, project=project, owner_id=current_user.id)


@router.get("/{project_id}", response_model=Project)
def read_project(
    project_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_project = get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if user has access to this project
    if current_user.role != "admin" and db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return db_project


@router.put("/{project_id}", response_model=Project)
def update_project_info(
    project_id: int,
    project_update: ProjectUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_project = get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if user has access to this project
    if current_user.role != "admin" and db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_project = update_project(db, project_id=project_id, project_update=project_update)
    return updated_project


@router.delete("/{project_id}")
def delete_project_by_id(
    project_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_project = get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if user has access to this project
    if current_user.role != "admin" and db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    delete_project(db, project_id=project_id)
    return {"message": "Project deleted successfully"} 