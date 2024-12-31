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
        data: {
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
        timeout: 300000
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
        timeout: 300000
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
        timeout: 300000
    });
}
// 人脸检测type字段检索  
export function getanalyzeType(data) {
    return request.request({
        url: `/image-analyze-type`,
        method: 'GET',
        params: {
            type:data.type
        }
    })
}
//官方人脸证件接口
export function getofficeFace(data) {
    return request.request({
        url: `/office-face`,
        method: 'GET',
        params: {
            page:data.page,
            page_size:data.page_size,
            start_time:data.start_time,
            end_time:data.end_time,
            status:data.status
        }
    })
}
// 官方人脸证件上传
export function UploadOfficeFace(data) {
    return request.request({
        url: '/office-face/upload',
        method: 'POST',
        data,
    });
}
// 官方人脸证件删除
export function DelOfficeFace(data) {
    return request.request({
        url: '/office-face/delete',
        method: 'POST',
        data,
    });
}