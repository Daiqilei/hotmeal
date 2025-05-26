/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type AdminUserUpdate = {
    /**
     * 新账号名
     */
    account?: string;
    /**
     * 新密码 (可选, 将被哈希)
     */
    password?: string;
    /**
     * 新角色
     */
    role?: AdminUserUpdate.role;
    /**
     * 新邮箱地址
     */
    email?: string;
    /**
     * 新手机号
     */
    phone_number?: string;
    /**
     * 新显示用户名
     */
    username?: string;
    /**
     * 新状态
     */
    status?: AdminUserUpdate.status;
    /**
     * 偏好的菜系
     */
    favorite_cuisine?: string;
};
export namespace AdminUserUpdate {
    /**
     * 新角色
     */
    export enum role {
        ADMIN = 'ADMIN',
        STAFF = 'STAFF',
        USER = 'USER',
    }
    /**
     * 新状态
     */
    export enum status {
        ACTIVE = 'ACTIVE',
        BANNED = 'BANNED',
        DELETED = 'DELETED',
    }
}

