/**
 * 统一的规划 API
 */

import { apiClient } from './config'

// ==================== 类型定义 ====================

export interface StructurePreference {
  parts: number
  volumes_per_part: number
  acts_per_volume: number
}

export interface MacroPlanRequest {
  target_chapters: number
  structure: StructurePreference
}

export interface ActChaptersRequest {
  chapter_count?: number
}

export interface ContinuePlanningRequest {
  current_chapter: number
}

// ==================== API ====================

export const planningApi = {
  // ==================== 宏观规划 ====================

  generateMacro: (novelId: string, data: MacroPlanRequest) =>
    apiClient.post(`/planning/novels/${novelId}/macro/generate`, data),

  confirmMacro: (novelId: string, data: { structure: any[] }) =>
    apiClient.post(`/planning/novels/${novelId}/macro/confirm`, data),

  // ==================== 幕级规划 ====================

  generateActChapters: (actId: string, data: ActChaptersRequest) =>
    apiClient.post(`/planning/acts/${actId}/chapters/generate`, data),

  confirmActChapters: (actId: string, data: { chapters: any[] }) =>
    apiClient.post(`/planning/acts/${actId}/chapters/confirm`, data),

  // ==================== AI 续规划 ====================

  continuePlanning: (novelId: string, data: ContinuePlanningRequest) =>
    apiClient.post(`/planning/novels/${novelId}/continue`, data),

  createNextAct: (actId: string) =>
    apiClient.post(`/planning/acts/${actId}/create-next`),

  // ==================== 查询 ====================

  getStructure: (novelId: string) =>
    apiClient.get(`/planning/novels/${novelId}/structure`),

  getActDetail: (actId: string) =>
    apiClient.get(`/planning/acts/${actId}`),

  getChapterDetail: (chapterId: string) =>
    apiClient.get(`/planning/chapters/${chapterId}`),
}
