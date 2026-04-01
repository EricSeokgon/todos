import traceback
import sys
try:
    from fastapi.testclient import TestClient
    from main import app
    import json

    client = TestClient(app)

    with open("test_out.txt", "w", encoding="utf-8") as f:
        f.write("--- 데이터 생성 테스트 시작 ---\n")
        # 새로운 할 일 생성
        payload = {"title": "FastAPI DB 연동 테스트", "is_done": False}
        post_response = client.post("/todos", json=payload)
        f.write(f"1) POST /todos 상태 코드: {post_response.status_code}\n")
        f.write(f"2) 생성된 데이터: {json.dumps(post_response.json(), ensure_ascii=False, indent=2)}\n")

        # 생성된 데이터가 전체 조회에 나오는지 확인
        get_response = client.get("/todos")
        f.write(f"\n3) GET /todos 상태 코드: {get_response.status_code}\n")
        f.write(f"4) 전체 조회 데이터 개수: {len(get_response.json())}\n")
        f.write(f"5) 전체 데이터 목록: {json.dumps(get_response.json(), ensure_ascii=False, indent=2)}\n")
        f.write("--- 데이터 생성 테스트 완료 ---\n")
except Exception as e:
    with open("test_out.txt", "w", encoding="utf-8") as f:
        f.write(traceback.format_exc())
