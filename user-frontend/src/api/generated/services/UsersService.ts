/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AdminUserUpdate } from '../models/AdminUserUpdate';
import type { AvatarUpdate } from '../models/AvatarUpdate';
import type { ProfileUpdate } from '../models/ProfileUpdate';
import type { Token } from '../models/Token';
import type { UserLogin } from '../models/UserLogin';
import type { UserOutput } from '../models/UserOutput';
import type { UserRegister } from '../models/UserRegister';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class UsersService {
    /**
     * 测试管理员权限的接口。
     * 只有拥有 ADMIN 角色的用户才能访问。
     * @returns any 权限验证通过
     * @throws ApiError
     */
    public static adminPermissionTest(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/admin/admin',
            errors: {
                401: `需要认证`,
                403: `需要管理员权限`,
            },
        });
    }
    /**
     * 列出所有活跃用户 (仅管理员)
     * @returns UserOutput 成功获取用户列表
     * @throws ApiError
     */
    public static adminListUsers(): CancelablePromise<Array<UserOutput>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/list',
            errors: {
                401: `需要认证`,
                403: `需要管理员权限`,
                500: `获取用户列表失败`,
            },
        });
    }
    /**
     * 验证用户身份并返回 JWT 令牌
     * @param payload
     * @returns Token 登录成功
     * @throws ApiError
     */
    public static loginUser(
        payload: UserLogin,
    ): CancelablePromise<Token> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/users/login',
            body: payload,
            errors: {
                401: `无效的账号或密码`,
                500: `登录失败`,
            },
        });
    }
    /**
     * 更新当前登录用户的头像 URL（需先上传图片）
     * @param payload
     * @returns any 头像更新成功，返回新头像链接
     * @throws ApiError
     */
    public static updateOwnAvatar(
        payload: AvatarUpdate,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/me/avatar',
            body: payload,
            errors: {
                400: `头像链接无效`,
                401: `需要认证`,
                404: `用户不存在`,
                500: `更新失败`,
            },
        });
    }
    /**
     * 更新当前登录用户的个人资料
     * @param payload
     * @returns UserOutput 个人资料更新成功
     * @throws ApiError
     */
    public static updateOwnProfile(
        payload: ProfileUpdate,
    ): CancelablePromise<UserOutput> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/profile',
            body: payload,
            errors: {
                400: `无效的输入数据`,
                401: `需要认证`,
                404: `User not found`,
                409: `邮箱/手机号/用户名冲突`,
                500: `更新个人资料失败`,
            },
        });
    }
    /**
     * 获取当前登录用户的个人资料
     * @returns UserOutput 成功获取个人资料
     * @throws ApiError
     */
    public static getOwnProfile(): CancelablePromise<UserOutput> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/profile',
            errors: {
                401: `需要认证`,
                404: `User not found`,
                500: `获取个人资料失败`,
            },
        });
    }
    /**
     * 注册一个新用户
     * @param payload
     * @returns UserOutput 用户注册成功
     * @throws ApiError
     */
    public static registerUser(
        payload: UserRegister,
    ): CancelablePromise<UserOutput> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/users/register',
            body: payload,
            errors: {
                400: `输入参数无效或角色无效`,
                409: `Account already exists`,
                500: `注册失败`,
            },
        });
    }
    /**
     * 更新指定用户的信息 (仅管理员)
     * @param userId 要管理的用户 ID
     * @param payload
     * @returns UserOutput 用户信息更新成功
     * @throws ApiError
     */
    public static adminUpdateUser(
        userId: number,
        payload: AdminUserUpdate,
    ): CancelablePromise<UserOutput> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/users/{user_id}',
            path: {
                'user_id': userId,
            },
            body: payload,
            errors: {
                400: `无效的输入数据`,
                401: `需要认证`,
                403: `需要管理员权限`,
                404: `User not found`,
                409: `账号/邮箱/手机号冲突`,
                500: `更新失败`,
            },
        });
    }
    /**
     * 获取指定用户的详细信息 (仅管理员)
     * @param userId 要管理的用户 ID
     * @returns UserOutput 用户已找到
     * @throws ApiError
     */
    public static adminGetUser(
        userId: number,
    ): CancelablePromise<UserOutput> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                401: `需要认证`,
                403: `需要管理员权限`,
                404: `User not found`,
                500: `获取用户失败`,
            },
        });
    }
    /**
     * Permanently deletes a specific user (hard delete, admin only)
     * @param userId 要管理的用户 ID
     * @returns void
     * @throws ApiError
     */
    public static adminDeleteUser(
        userId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                401: `Authentication required`,
                403: `Admin privileges required`,
                404: `User not found`,
                409: `Cannot delete user, possibly due to related data`,
                500: `Deletion failed`,
            },
        });
    }
}
