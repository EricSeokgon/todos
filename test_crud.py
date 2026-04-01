import random
import json
import traceback
from fastapi.testclient import TestClient
from main import app

try:
    client = TestClient(app)
    
    with open("crud_res.txt", "w", encoding="utf-8") as f:
        f.write("--- CRUD 테스트 시작 ---\n\n")
        
        # 1. 랜덤하게 3개의 데이터 생성
        titles = ["장보기", "운동하기", "코딩 공부", "책 읽기", "방 청소", "이메일 답장", "친구 만나기"]
        selected_titles = random.sample(titles, 3)
        
        created_ids = []
        for i, title in enumerate(selected_titles):
            resp = client.post("/todos", json={"title": title, "is_done": False})
            data = resp.json()
            created_ids.append(data["id"])
            f.write(f"[생성 {i+1}] {data['title']} (ID: {data['id']})\n")
            
        f.write("\n")
        
        # 2. 조회 결과 확인
        resp = client.get("/todos")
        all_todos = resp.json()
        f.write(f"[전체 조회] 현재 데이터 개수: {len(all_todos)}\n")
        
        # 3. 데이터 수정 테스트 (마지막 생성한 Todo를 수정)
        update_id = created_ids[-1]
        f.write(f"\n[수정] ID {update_id}의 내용을 수정합니다...\n")
        patch_resp = client.patch(f"/todos/{update_id}", json={"title": "수정된 타이틀!", "is_done": True})
        if patch_resp.status_code == 200:
            patched_data = patch_resp.json()
            f.write(f" -> 성공적으로 수정됨: {patched_data['title']} (is_done={patched_data['is_done']})\n")
        else:
            f.write(f" -> 수정 실패! 상태 코드: {patch_resp.status_code}\n")
            
        # 4. 데이터 삭제 테스트 (첫번째 생성한 Todo를 삭제)
        delete_id = created_ids[0]
        f.write(f"\n[삭제] ID {delete_id}의 데이터를 삭제합니다...\n")
        del_resp = client.delete(f"/todos/{delete_id}")
        if del_resp.status_code == 204:
            f.write(" -> 성공적으로 삭제됨 (204 NO_CONTENT)\n")
        else:
            f.write(f" -> 삭제 실패! 상태 코드: {del_resp.status_code}\n")
            
        # 5. 최종 결과 확인
        final_resp = client.get("/todos")
        final_todos = final_resp.json()
        f.write(f"\n[최종 조회] 변경 후 데이터 개수: {len(final_todos)}\n")
        f.write(f"[최종 데이터 목록]: {json.dumps(final_todos, ensure_ascii=False, indent=2)}\n")
        
        f.write("\n--- CRUD 테스트 완료 ---\n")

except Exception as e:
    with open("crud_res.txt", "w", encoding="utf-8") as f:
        f.write(traceback.format_exc())
