/**
 * @file            src/api/tag.js
 * @description
 * @author          taichilei
 * @date            2025-05-24
 * @version         1.0.0
 */

import request from '../utils/request'


// 获取标签列表（支持分页或不分页，统一走 /tags 接口）
export function getTagList(params) {
  return request({
    url: '/tags',
    method: 'GET',
    params
  })
}

// 新建标签
export function createTag(data) {
  return request({
    url: '/tags',
    method: 'POST',
    data
  })
}

// 更新标签
export function updateTag(tagId, data) {
  return request({
    url: `/tags/${tagId}`,
    method: 'PUT',
    data
  })
}

// 删除标签
export function deleteTagById(tagId) {
  return request({
    url: `/tags/${tagId}`,
    method: 'DELETE'
  })
}

// 获取全部标签（用于下拉选择等场景）
export function getAllTags() {
  return request({
    url: '/tags',
    method: 'GET'
  })
}
