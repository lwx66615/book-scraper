import json
from pathlib import Path
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SiteRule
from app.schemas import SiteRuleCreate, SiteRuleUpdate
from app.crawlers.generic_adapter import GenericSiteAdapter


class RuleService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.rules_path = Path("rules/default_rules.json")

    async def get_list(self) -> List[SiteRule]:
        """获取规则列表"""
        result = await self.session.execute(
            select(SiteRule).order_by(SiteRule.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, rule_id: int) -> Optional[SiteRule]:
        """根据ID获取规则"""
        result = await self.session.execute(
            select(SiteRule).where(SiteRule.id == rule_id)
        )
        return result.scalar_one_or_none()

    async def create(self, rule_data: SiteRuleCreate) -> SiteRule:
        """创建规则"""
        rule = SiteRule(**rule_data.model_dump())
        self.session.add(rule)
        await self.session.commit()
        await self.session.refresh(rule)
        return rule

    async def update(self, rule_id: int, rule_data: SiteRuleUpdate) -> Optional[SiteRule]:
        """更新规则"""
        rule = await self.get_by_id(rule_id)
        if not rule:
            return None

        update_data = rule_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(rule, key, value)

        await self.session.commit()
        await self.session.refresh(rule)
        return rule

    async def delete(self, rule_id: int) -> bool:
        """删除规则"""
        rule = await self.get_by_id(rule_id)
        if not rule:
            return False

        await self.session.delete(rule)
        await self.session.commit()
        return True

    async def test_rule(self, rule_id: Optional[int], test_url: str) -> dict:
        """测试规则"""
        if rule_id:
            rule = await self.get_by_id(rule_id)
            if not rule:
                return {"success": False, "message": "规则不存在"}

            rule_config = {
                "selectors": rule.selectors,
                "headers": rule.headers,
                "requires_js": rule.requires_js
            }
        else:
            rule_config = None

        adapter = GenericSiteAdapter(rule_config)

        try:
            # 测试获取小说信息
            novel_info = await adapter.get_novel_info(test_url)

            # 测试获取章节列表（只取前5个）
            chapters = await adapter.get_chapter_list(test_url)
            sample_chapters = chapters[:5]

            # 测试获取章节内容（只测试第一个）
            sample_content = None
            if sample_chapters:
                content = await adapter.get_chapter_content(sample_chapters[0].url)
                sample_content = {
                    "title": content.title,
                    "content_preview": content.content[:200] if content.content else None
                }

            await adapter.close()

            return {
                "success": True,
                "message": "规则测试成功",
                "extracted_data": {
                    "novel_info": {
                        "title": novel_info.title,
                        "author": novel_info.author,
                        "status": novel_info.status
                    },
                    "chapters_count": len(chapters),
                    "sample_chapters": [{"index": c.index, "title": c.title} for c in sample_chapters],
                    "sample_content": sample_content
                }
            }

        except Exception as e:
            await adapter.close()
            return {"success": False, "message": str(e)}

    def load_default_rules(self) -> List[dict]:
        """从配置文件加载默认规则"""
        if not self.rules_path.exists():
            return []

        with open(self.rules_path, "r", encoding="utf-8") as f:
            return json.load(f)
