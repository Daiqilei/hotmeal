/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type UserRegister = {
    /**
     * 用户账号名 (必须唯一)
     */
    account: string;
    /**
     * 用户密码
     */
    password: string;
    /**
     * 用户角色 (USER 或 ADMIN)
     */
    role?: UserRegister.role;
};
export namespace UserRegister {
    /**
     * 用户角色 (USER 或 ADMIN)
     */
    export enum role {
        ADMIN = 'ADMIN',
        USER = 'USER',
    }
}

