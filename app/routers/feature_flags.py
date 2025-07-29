from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import get_current_active_user
from ..crud import (
    get_feature_flags, get_feature_flag, create_feature_flag, 
    update_feature_flag, delete_feature_flag, get_project,
    get_feature_flag_by_name_and_project
)
from ..schemas import FeatureFlag, FeatureFlagCreate, FeatureFlagUpdate
from ..models import User as UserModel, Environment

router = APIRouter(prefix="/feature-flags", tags=["feature flags"])


@router.get("/", response_model=List[FeatureFlag])
def read_feature_flags(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    environment: Optional[Environment] = Query(None, description="Filter by environment"),
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # If project_id is specified, check if user has access to that project
    if project_id:
        db_project = get_project(db, project_id=project_id)
        if db_project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        
        if current_user.role != "admin" and db_project.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    flags = get_feature_flags(
        db, 
        skip=skip, 
        limit=limit, 
        project_id=project_id,
        environment=environment
    )
    return flags


@router.post("/", response_model=FeatureFlag)
def create_new_feature_flag(
    flag: FeatureFlagCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if user has access to the project
    db_project = get_project(db, project_id=flag.project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if current_user.role != "admin" and db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if feature flag with same name already exists in the project
    existing_flag = get_feature_flag_by_name_and_project(db, flag.name, flag.project_id)
    if existing_flag:
        raise HTTPException(
            status_code=400, 
            detail="Feature flag with this name already exists in this project"
        )
    
    return create_feature_flag(db=db, flag=flag, created_by_id=current_user.id)


@router.get("/{flag_id}", response_model=FeatureFlag)
def read_feature_flag(
    flag_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_flag = get_feature_flag(db, flag_id=flag_id)
    if db_flag is None:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    # Check if user has access to the project
    db_project = get_project(db, project_id=db_flag.project_id)
    if current_user.role != "admin" and db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return db_flag


@router.put("/{flag_id}", response_model=FeatureFlag)
def update_feature_flag_info(
    flag_id: int,
    flag_update: FeatureFlagUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_flag = get_feature_flag(db, flag_id=flag_id)
    if db_flag is None:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    # Check if user has access to the project
    db_project = get_project(db, project_id=db_flag.project_id)
    if current_user.role != "admin" and db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_flag = update_feature_flag(db, flag_id=flag_id, flag_update=flag_update)
    return updated_flag


@router.delete("/{flag_id}")
def delete_feature_flag_by_id(
    flag_id: int,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_flag = get_feature_flag(db, flag_id=flag_id)
    if db_flag is None:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    # Check if user has access to the project
    db_project = get_project(db, project_id=db_flag.project_id)
    if current_user.role != "admin" and db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    delete_feature_flag(db, flag_id=flag_id)
    return {"message": "Feature flag deleted successfully"}


@router.get("/project/{project_id}", response_model=List[FeatureFlag])
def read_project_feature_flags(
    project_id: int,
    environment: Optional[Environment] = Query(None, description="Filter by environment"),
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if user has access to the project
    db_project = get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if current_user.role != "admin" and db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    flags = get_feature_flags(
        db, 
        project_id=project_id,
        environment=environment
    )
    return flags 