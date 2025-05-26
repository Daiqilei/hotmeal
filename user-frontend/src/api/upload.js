/**
 * @file         src/api/upload.js
 * @author       taichilei
 * @date         2025-04-30
 * @description
 */
import {request} from '@/utils/request'

/**
 * 上传图片（例如头像、支付凭证等）
 * @param {File} file 图片文件
 * @returns {Promise}
 */
export function uploadImage(file) {
    const formData = new FormData()
    formData.append('file', file)

    return request.post('/upload/image', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
}