from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.services.rule_service import RuleService
from app.schemas import (
    SiteRuleCreate, SiteRuleUpdate, SiteRuleResponse,
    SiteRuleListResponse, RuleTestRequest, RuleTestResult, MessageResponse
)

router = APIRouter()


def get_rule_service(session: AsyncSession = Depends(get_session)) -> RuleService:
    return RuleService(session)


@router.get("", response_model=SiteRuleListResponse)
async def get_rules(
    service: RuleService = Depends(get_rule_service)
):
    """获取规则列表"""
    rules = await service.get_list()
    return SiteRuleListResponse(
        items=[SiteRuleResponse.model_validate(r) for r in rules],
        total=len(rules)
    )


@router.get("/{rule_id}", response_model=SiteRuleResponse)
async def get_rule(
    rule_id: int,
    service: RuleService = Depends(get_rule_service)
):
    """获取规则详情"""
    rule = await service.get_by_id(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="规则不存在")
    return SiteRuleResponse.model_validate(rule)


@router.post("", response_model=SiteRuleResponse)
async def create_rule(
    rule_data: SiteRuleCreate,
    service: RuleService = Depends(get_rule_service)
):
    """创建规则"""
    rule = await service.create(rule_data)
    return SiteRuleResponse.model_validate(rule)


@router.put("/{rule_id}", response_model=SiteRuleResponse)
async def update_rule(
    rule_id: int,
    rule_data: SiteRuleUpdate,
    service: RuleService = Depends(get_rule_service)
):
    """更新规则"""
    rule = await service.update(rule_id, rule_data)
    if not rule:
        raise HTTPException(status_code=404, detail="规则不存在")
    return SiteRuleResponse.model_validate(rule)


@router.delete("/{rule_id}", response_model=MessageResponse)
async def delete_rule(
    rule_id: int,
    service: RuleService = Depends(get_rule_service)
):
    """删除规则"""
    success = await service.delete(rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="规则不存在")
    return MessageResponse(message="删除成功")


@router.post("/test", response_model=RuleTestResult)
async def test_rule(
    request: RuleTestRequest,
    service: RuleService = Depends(get_rule_service)
):
    """测试规则"""
    result = await service.test_rule(request.rule_id, request.test_url)
    return RuleTestResult(**result)
