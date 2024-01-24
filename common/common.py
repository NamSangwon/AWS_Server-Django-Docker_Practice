from rest_framework.views import APIView
from rest_framework.response import Response

############################ 공통 영역 ############################

# 해당 공통 클래스를 사용 시 APIView의 기능을 포함하여 새로 정의한 기능을 추가로 사용 가능
class TodoView(APIView): 
    user_id = ''
    version = '' # 사용자가 사용하는 버전이 모두 같지 않음 -> 해당 버전에 맞는 백엔드 코드를 실행함

    # Get || Post || etx... 중 어느 것으로 왔는 지 확인하는 함수
    # TodoView.dispatch() 실행 -> (사전 작업 (ex. 아래의 headers 값 받아 오기)) -> 상속한 APIView.dispatch() 실행 
    def dispatch(self, request, *args, **kwargs):
        # body 부에 담아 오던 user_id와 version을 header에 담도록 변경 (더 유용하게 하기 위함)
        self.user_id = request.headers.get('id', False) # 입력받은 id가 있으면 self.user_id에 저장하고, 없으면 저장 X
        self.version = request.headers.get('version', '1.0') # 버전 = 입력 받은 버전, 입력 받은 값이 없으면 1.0 

        return super(TodoView, self).dispatch(request, *args, **kwargs)

    pass

# 출력을 공통 포맷으로 수정하기 위해 공통 클래스 생성
def CommonResponse(result_code, result_msg, data):
    return Response(status=200,
                    data=dict(
                        result_code=result_code,
                        result_msg=result_msg,
                        data=data
                    ))

def SuccessResponse():
    return Response(status=200,
                    data=dict(
                        result_code=0,
                        result_msg="success"
                    ))

def SuccessResponseWithData(data):
    return Response(status=200,
                    data=dict(
                        result_code=0,
                        result_msg="success",
                        data=data
                    ))

def ErrorResponse():
    return Response(status=200,
                    data=dict(
                        result_code=999,
                        result_msg="Error!!"
                    ))