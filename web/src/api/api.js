import request from "../untis/request.js";

export function login(data) {
    return request.request({
        url: '/login',
        method: 'POST',
        data,
    })
}
// 获取测试接口列表 
export function gettestApi(data) {
    return request.request({
        url: `/test-api${data ? '/' + data : ''}`,
        method: 'GET',
    })
}
// 新建接口
export function settestApi(data) {
    return request.request({
        url: '/test-api',
        method: 'POST',
        data,
    })
}
// 修改接口
export function modifytestApi(data) {
    return request.request({
        url: '/test-api',
        method: 'PUT',
        data,
    })
}
// 删除接口 
export function DeltestApi(data) {
    return request.request({
        url: `/test-api`,
        method: 'DELETE',
        params: {
            id: data.id
        }
    })
}
// 解密md5
export function Md5decode(data) {
    return request.request({
        url: '/decrypt-md5',
        method: 'POST',
        data,
    })
}

//创建任务
export function createTask(data) {
    return request.request({
        url: '/test-task',
        method: 'POST',
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        data,
    });
}

// 获取任务列表
export function getTasklist(data) {
    return request.request({
        url: `/test-task`,
        method: 'GET',
        params: {
            id: data.id,
            status:data.status,
            task_name:data.task_name,
            uname:data.uname
        }
    })
}
// 删除任务
export function DelTasklist(data) {
    return request.request({
        url: `/test-task`,
        method: 'DELETE',
        params: {
            id: data.id
        }
    })
}
// 修改任务
export function modifyTask(data) {
    return request.request({
        url: '/test-task',
        method: 'PUT',
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        data,
    })
}
// 下载测试结果文件
export function downFile(data) {
    return request.request({
        url: `/test-task/download`,
        method: 'GET',
        params: {
            id: data.id
        },
        responseType: 'blob' ,
        headers: {
            'Cache-Control': 'no-cache'
          }
        
    })
}

// 公告获取
export function announcement() {
    return request.request({
        url: `/announcement`,
        method: 'GET',
    })
}

//人脸识别 
export function ImageAnalyze(data) {
    return request.request({
        url: '/image-analyze',
        method: 'POST',
        data,
    });
}