import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
import certifi
import os

# SSL 인증서 경로 설정
os.environ['SSL_CERT_FILE'] = certifi.where()

st.title("🎓 KB 교과세특 작문 도우미")

# API 키 입력
api_key = st.text_input("Google API Key를 입력하세요", type="password")

if api_key:
    # 입력 필드 생성
    st.subheader("활동 정보 입력")
    subject = st.text_input("단원명")
    activity = st.text_input("활동명")
    content = st.text_area("활동 내용")
    project = st.text_area("개인 프로젝트 (활동을 통해 얻은 역량)")
    learning = st.text_area("배운 점")

    # 생성 버튼
    if st.button("교과세특 생성하기"):
        try:
            # Gemini 모델 설정
            llm = GoogleGenerativeAI(model="gemini-1.0-pro", google_api_key=api_key)
            
            # 프롬프트 템플릿 설정
            template = """
            다음 정보를 바탕으로 고등학교 교과세특을 작성해주세요.
            
            조건:
            1. 모든 문장은 명사형으로 종료
            2. 문장과 문장 사이는 다음과 같은 연결어를 활용하여 자연스럽게 연결
               - "이 과정에서..."
               - "특히..."
               - "더불어..."
               - "나아가..."
               - "이를 바탕으로..."
               - "이를 통한..."
            3. 전체적으로 하나의 완성된 글로 작성
            4. 첫 문장은 "[단원명] 단원에서 '심도 있는/적극적인/창의적인/주도적인/열정적인' 등의 긍정적 수식어와 함께 [활동명]..." 형식으로 시작
            5. 개인 프로젝트는 다음과 같은 형식으로 긍정적으로 표현
               - "이러한 학습을 바탕으로 한 개인 프로젝트를 통한 [프로젝트 내용]의 성공적 수행"
               - "심화 학습의 결과로 진행한 개인 프로젝트에서의 [프로젝트 내용]에 대한 탁월한 성취"
               - "배운 내용을 응용한 개인 프로젝트에서의 [프로젝트 내용]의 우수한 구현"
            6. 마지막 문장은 다음과 같은 형식으로 배운점을 긍정적으로 표현하고 명사형으로 종료
               - "궁극적으로 [배운점]에 대한 깊이 있는 통찰력의 함양"
               - "나아가 [배운점]에 대한 탁월한 역량의 체득"
               - "더불어 [배운점]에 대한 전문적 지식의 습득"
               - "결과적으로 [배운점]에 대한 실질적 능력의 배양"
            
            단원명: {subject}
            활동명: {activity}
            활동 내용: {content}
            활동 역량: {project}
            종합 역량: {learning}
            
            결과는 200자 이내의 하나의 문단으로 작성해주세요.
            
            작성 예시:
            "[단원명] 단원에서 심도 있는 [활동명]의 수행. 이 과정에서 [구체적인 활동]에 대한 탐구. 특히 심화 학습의 결과로 진행한 개인 프로젝트에서의 [프로젝트 내용]에 대한 탁월한 성취. 궁극적으로 [배운점]에 대한 깊이 있는 통찰력의 함양."
            
            배운점 관련 긍정적 종결 표현:
            - 깊이 있는 통찰력의 함양
            - 탁월한 역량의 체득
            - 전문적 지식의 습득
            - 실질적 능력의 배양
            - 종합적 사고력의 확장
            - 창의적 문제해결력의 증진
            - 혁신적 접근법의 발견
            - 체계적 분석력의 향상
            
            주의사항:
            - '~하였음', '~했음' 등의 종결어미 사용 금지
            - '~의 수행', '~의 달성', '~의 함양' 등 명사형 종결 필수
            - 수식어는 자연스럽게 문맥에 맞게 선택하여 사용
            - 연결어를 적절히 활용하여 문장 간 자연스러운 흐름 유지
            - 개인 프로젝트는 반드시 긍정적인 성과로 표현
            - 마지막 문장은 배운점을 긍정적이고 전문적인 표현으로 종료
            """
            
            prompt = PromptTemplate(
                input_variables=["subject", "activity", "content", "project", "learning"],
                template=template
            )
            
            # 최신 LangChain 방식으로 체인 실행
            chain = prompt | llm
            
            # 결과 생성
            result = chain.invoke({
                "subject": subject,
                "activity": activity,
                "content": content,
                "project": project,
                "learning": learning
            })
            
            # 결과 출력
            st.subheader("생성된 교과세특")
            st.write(result)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
else:
    st.warning("API 키를 입력해주세요.")
