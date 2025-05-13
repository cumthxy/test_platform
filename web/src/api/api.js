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
//下载文件
export function downFiletwo(data) {
    return request.request({
        url: `/test-task/download-data `,
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
        url: '/office-face/batch-upload',
        method: 'POST',
        data,
    });
}
// 官方人脸证件删除
export function DelOfficeFace(data) {
    return request.request({
        url: '/office-face/batch-delete',
        method: 'POST',
        data,
    });
}

// 官方人脸证件删除
export function confirmOfficeFace(data) {
    return request.request({
        url: '/office-face/batch-confirm',
        method: 'POST',
        data,
    });
}


// 假证确认列表接口
export function getfakeIdcard(data) {
    return request.request({
        url: `/fake-id-card`,
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
// 假证确认 
export function faceOperation(data) {
    return request.request({
        url: '/fake-id-card/batch-operation',
        method: 'POST',
        data,
    });
}
// 风险人脸二次确认
export function getRiskFace(data) {
    return request.request({
        url: `/risk_face`,
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
// 风险人脸确认接口
export function RiskfaceOperation(data) {
    return request.request({
        url: '/risk_face/batch-operation',
        method: 'POST',
        data,
    });
}

// 下载md5图片
export function downMd5(data) {
    return request.request({
        url: '/image-analyze-md5download',
        method: 'POST',
        data
    })
}

// 获取md5_type
export function getMd5Type() {
    return request.request({
        url: '/image-analyze-md5type',
        method: 'GET',
  
    })
}