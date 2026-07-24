from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from app.enums import RunStatus


class RunCreateRequestInput(BaseModel):
    """创建agent任务参数"""
    ticket_id: str = Field(..., description="工单ID")
    order_id: str = Field(..., description="订单ID")
    customer_message: str = Field(..., description="客户消息")

class RunCreateRequest(BaseModel):
    """创建agent任务请求"""
    run_type: str = Field(..., description="任务类型")
    idempotency_key: str = Field(..., description="幂等性键")
    input: RunCreateRequestInput = Field(..., description="输入参数")

class RunCreateResponse(BaseModel):
    """创建agent任务响应"""
    run_id: str = Field(..., description="任务ID")
    status: RunStatus = Field(..., description="任务状态")
    run_type: str = Field(..., description="任务类型")
    created_at: datetime = Field(..., description="任务创建时间")

class RunGetRequestInput(BaseModel):
    """获取agent任务参数"""
    ticket_id: str = Field(..., description="工单ID")
    order_id: str = Field(..., description="订单ID")

class RunGetRequest(BaseModel):
    """获取agent任务响应"""
    run_id: str = Field(..., description="任务ID")
    status: RunStatus = Field(..., description="任务状态")
    run_type: str = Field(..., description="任务类型")
    input: RunGetRequestInput = Field(..., description="输入参数")
    output: Optional[str] = Field(None, description="输出结果")
    error: Optional[str] = Field(None, description="错误信息")
    created_at: datetime = Field(..., description="任务创建时间")
    updated_at: datetime = Field(..., description="任务更新时间")
    ended_at: Optional[datetime] = Field(None, description="任务结束时间")

class RunCancelRequest(BaseModel):
    """取消agent任务请求"""
    reason: str = Field(..., description="取消原因")

class RunCancelResponse(BaseModel):
    """取消agent任务响应"""
    run_id: str = Field(..., description="任务ID")
    status: RunStatus = Field(..., description="任务状态")

class RunResumeInput(BaseModel):
    """用户补充后，恢复agent任务参数"""
    user_message: str = Field(..., description="用户消息")

class RunResumeRequest(BaseModel):
    """用户补充后，恢复agent任务请求"""
    user_input: RunResumeInput = Field(..., description="用户输入")

class RunResumeResponse(BaseModel):
    """用户补充后，恢复agent任务响应"""
    run_id: str = Field(..., description="任务ID")
    status: RunStatus = Field(..., description="任务状态")