##接口说明
	音频识别分类，将长段音频分类，音频分类（非实时）。 
	该接口是通过API的方式给开发者提供一个通用的HTTPS接口。
	音频时长返回时间可以参考下表:
	音频时长X（分钟）	参考返回时间Y（分钟）
	X<10			Y<3
	10<=X<30		3<=Y<6

###接口要求
集成语音转写API时，需按照以下要求。
内容		说明
请求协议	http[s]：HTTPS
请求地址	http[s]: https://nessos.cn/audio/ 
请求方式	POST
接口鉴权	暂无
字符编码	UTF-8
响应格式	统一采用JSON格式
开发语言	任意，只要可以向服务发起HTTPS请求的均可
音频属性	采样率16k或8k、位长8bit或16bit
音频格式	wav
音频大小	不超过4M
音频时长	不超过30分钟
语言种类	中文普通话
结果保存时长	当次请求有效

###处理接口
Step 1
    说明：将需要处理的wav文件上传，得到一个searchid（用于获取处理结果）
    URL
    POST  https://nessos.cn/audio/ 
    请求头
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    参数        类型           说明               示例
    wavname    file			  需要处理的文件      test.wav

    ###返回值
    {
        "status": 0,
        "filename": "test3.wav",
        "searchid": "c2f644779acde9f7961efab3ce27c3a0",
        "inputtime": "2021-12-05 00:07:23"
    }

Step 2
    说明：使用searchid来获取处理结果
    URL
    GET  https://nessos.cn/audio/search/?searchid=c2f644779acde9f7961efab3ce27c3a0
    请求头
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    参数        类型           说明                       示例
    searchid   string         wav文件处理结果的查询id      c2f644779acde9f7961efab3ce27c3a0

    ###返回值
    {
    "status": 0,
    "searchid": "c2f644779acde9f7961efab3ce27c3a0",
    "filename": "test3.wav",
    "createtime": "2021-12-05 00:07:23",
    "endtime": "2021-12-05 00:08:22",
    "data": [
        {
            "end": "16.65",
            "data": "嗯",
            "index": 0,
            "start": "7.17",
            "category": [
                {
                    "index": 0,
                    "result": "搞笑"
                },
                {
                    "index": 1,
                    "result": "宠物"
                },
                {
                    "index": 2,
                    "result": "美文"
                }
            ]
        },
        {
            "end": "27.12",
            "data": "嗯",
            "index": 1,
            "start": "16.68",
            "category": [
                {
                    "index": 0,
                    "result": "搞笑"
                },
                {
                    "index": 1,
                    "result": "宠物"
                },
                {
                    "index": 2,
                    "result": "美文"
                }
            ]
        }
    ]
}