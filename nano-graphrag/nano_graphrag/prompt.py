"""
Reference:
 - Prompts are from [graphrag](https://github.com/microsoft/graphrag)
"""

GRAPH_FIELD_SEP = "<SEP>"
PROMPTS = {}

PROMPTS[
    "claim_extraction"
] = """- Target Activity -
You are an intelligent assistant that helps a human analyst extract and analyze artistic claims made between entities found in the lyrics of Trịnh Công Sơn’s songs.

You are an expert in Vietnamese literature and music, specializing in identifying symbolic, poetic, and artistic relationships between characters, objects, and motifs across different artistic lenses (e.g., time, space, gender, nature, orientalism, existentialism, etc.).

- Goal -
Given a text document (typically song lyrics), along with a predefined entity specification and claim criteria, extract:
1. All relevant entities that match the specification
2. All claims made between or about these entities, grounded in the artistic context of the lyrics.

- Steps -
1. **Entity Extraction**  
   Extract all named entities that match the **entity specification**, which can include:
   - A list of specific entity names (e.g., “Mưa”, “Người mẹ”, “Chiều”)
   - A list of general entity types (e.g., person, natural_element, object, space)

2. **Claim Extraction**  
   For each identified entity, extract all valid claims. Each claim must follow the structure below:

   - **Subject**: Name of the entity making or representing the symbolic or poetic action. Must be one of the extracted entities.
   - **Object**: Name of the entity affected by the claim or referenced by it. If unknown or symbolic, return **NONE**.
   - **Claim Type**: A reusable, capitalized label that categorizes the type of artistic relationship. Example values:  
     `SYMBOLIC_REFLECTION`, `EMOTIONAL_PROJECTION`, `TEMPORAL_COLLAPSE`, `GENDERED_REMEMBRANCE`, etc.
   - **Claim Status**: One of the following:
     - `TRUE`: The symbolic relationship is explicitly or strongly implied in the lyrics.
     - `FALSE`: The claim is contradicted or not supported.
     - `SUSPECTED`: The claim is interpretive or weakly implied.
   - **Claim Description**: A detailed explanation grounded in artistic reasoning.  
     Include references to applicable **artistic lenses** and **sublenses** (e.g., `nature_as_emotion_mirror`, `feminine_subjectivity`, `psychological_space`) and justify your interpretation with analysis.
   - **Claim Year**: A time period relevant to the symbolic claim in ISO-8601 format.  
     Format: `start_date`, `end_date`. If only one date is known, use it for both. If unknown, return **NONE**.
   - **Claim Source Text**: A list of all Vietnamese **lyric quotes** from the original text that directly support the claim.

Format each claim as (<subject_entity>{tuple_delimiter}<object_entity>{tuple_delimiter}<claim_type>{tuple_delimiter}<claim_status>{tuple_delimiter}<claim_start_date>{tuple_delimiter}<claim_end_date>{tuple_delimiter}<claim_description>{tuple_delimiter}<claim_source>)

3. **Output Formatting**  
- Return all claims as a single list, separated by **{record_delimiter}**
- End the output with **{completion_delimiter}**

- Additional Notes -
- Write all content in **English**, except for `claim_source`, Subject, Object quotes, which should remain in **Vietnamese**.
- Avoid speculation. All claims must be based on direct lyrics and/or symbolic relationships grounded in the artistic lenses provided.
- If a relationship is deeply embedded or metaphorical, clearly state the interpretive reasoning in the `claim_description`.

###############################
-Lăng kính nghệ thuật-
###############################
Below are the artistic lenses (sub-lenses) relevant to the analysis that must be referred to during entity extraction:

I. Lăng kính Thời gian
   1. Thời gian tuyến tính (Linear Time)
   2. Thời gian phi tuyến tính (Non-Linear Time)
   3. Thời gian vòng lặp (Cyclical Time)
   4. Thời gian tĩnh (Frozen Time)
   5. Thời gian vỡ vụn (Fragmented Time)
   6. Thời gian nghịch lý (Paradoxical Time)
   7. Thời gian mang tính tâm lý (Psychological Time)
   8. Thời gian mang tính biểu tượng (Symbolic Time)

II. Lăng kính Không gian
   1. Không gian địa lý (Geographical Space)
   2. Không gian biểu tượng (Symbolic Space)
   3. Không gian tâm lý (Psychological Space)
   4. Không gian thiên nhiên (Nature Space)
   5. Không gian siêu thực (Surreal Space)
   6. Không gian lịch sử (Historical Space)
   7. Không gian bị giới hạn và bức bối (Constrained Space)
   8. Không gian mở và tự do (Expansive Space)
   9. Không gian thiêng liêng (Sacred Space)
   10. Không gian phân mảnh (Fragmented Space)

III. Lăng kính Thiên nhiên
   1. Thiên nhiên như tấm gương nội tâm (Nature as Mirror of Emotion)
   2. Thiên nhiên như đối tượng siêu hình (Nature as a Metaphysical Entity)
   3. Thiên nhiên như biểu tượng luân hồi & vô thường (Nature as Impermanence)
   4. Thiên nhiên như hồi ức ký ức (Nature as Mnemonic Landscape)
   5. Thiên nhiên như biểu tượng quê hương & đất mẹ (Nature as Homeland)
   6. Thiên nhiên như nơi trú ngụ cuối cùng (Nature as Refuge or Return)

IV. Lăng kính Giới
   1. Nữ thể tính (Feminine Subjectivity)
   2. Cơ thể nữ tính (Feminine Body and Eroticism)
   3. Giới và chiến tranh (Gendered Experience of War)

V. Lăng kính Chủ nghĩa Phương Đông (Orientalism)
   1. Phong vị phương Đông trong thẩm mỹ (Eastern Aestheticism)
   2. Đông như là bản sắc đối lập Tây (East vs. West Identity)
   3. Tự nhiên và Đông phương luận (Nature and the East)
   4. Tâm linh và tính thiêng (Spiritual Orientalism)

VI. Lăng kính Existentialism
   1. Tha hóa con người trong xã hội sản xuất (Alienation from Capitalist Society)
   2. Công cụ hóa cơ thể – vật hóa con người (Reification and Objectification)
   3. Phê phán xã hội công nghiệp hóa (Critique of Industrialization and Modernity)
   4. Chiến tranh như sản phẩm của chủ nghĩa tư bản toàn cầu (War as Imperialist-Capitalist Structure)
   5. Cảm giác mất căn tính trong đô thị hóa – thị trường hóa (Identity Crisis under Urbanization and Market Logic)
   6. Kháng cự tiêu dùng & vật chất (Anti-consumerism & Spiritual Emptiness)

- Goal -
Given a text document (typically song lyrics), along with a predefined entity specification and claim criteria, extract:
1. All relevant entities that match the specification
2. All claims made between or about these entities, grounded in the artistic context of the lyrics.

- Steps -
1. **Entity Extraction**  
   Extract all named entities that match the **entity specification**, which can include:
   - A list of specific entity names (e.g., “Mưa”, “Người mẹ”, “Chiều”)
   - A list of general entity types (e.g., person, natural_element, object, space)

2. **Claim Extraction**  
   For each identified entity, extract all valid claims. Each claim must follow the structure below:

   - **Subject**: Name of the entity making or representing the symbolic or poetic action. Must be one of the extracted entities.
   - **Object**: Name of the entity affected by the claim or referenced by it. If unknown or symbolic, return **NONE**.
   - **Claim Type**: A reusable, capitalized label that categorizes the type of artistic relationship. Example values:  
     `SYMBOLIC_REFLECTION`, `EMOTIONAL_PROJECTION`, `TEMPORAL_COLLAPSE`, `GENDERED_REMEMBRANCE`, etc.
   - **Claim Status**: One of the following:
     - `TRUE`: The symbolic relationship is explicitly or strongly implied in the lyrics.
     - `FALSE`: The claim is contradicted or not supported.
     - `SUSPECTED`: The claim is interpretive or weakly implied.
   - **Claim Description**: A detailed explanation grounded in artistic reasoning.  
     Include references to applicable **artistic lenses** and **sublenses** (e.g., `nature_as_emotion_mirror`, `feminine_subjectivity`, `psychological_space`) and justify your interpretation with analysis.
   - **Claim Year**: A time period relevant to the symbolic claim in ISO-8601 format.  
     Format: `start_date`, `end_date`. If only one date is known, use it for both. If unknown, return **NONE**.
   - **Claim Source Text**: A list of all Vietnamese **lyric quotes** from the original text that directly support the claim.

Format each claim as (<subject_entity>{tuple_delimiter}<object_entity>{tuple_delimiter}<claim_type>{tuple_delimiter}<claim_status>{tuple_delimiter}<claim_start_date>{tuple_delimiter}<claim_end_date>{tuple_delimiter}<claim_description>{tuple_delimiter}<claim_source>)

3. **Output Formatting**  
- Return all claims as a single list, separated by **{record_delimiter}**
- End the output with **{completion_delimiter}**

- Additional Notes -
- Write all content in **English**, except for `claim_source`, Subject, Object quotes, which should remain in **Vietnamese**.
- Avoid speculation. All claims must be based on direct lyrics and/or symbolic relationships grounded in the artistic lenses provided.
- If a relationship is deeply embedded or metaphorical, clearly state the interpretive reasoning in the `claim_description`.

- Goal -
Given a text document (typically song lyrics), along with a predefined entity specification and claim criteria, extract:
1. All relevant entities that match the specification
2. All claims made between or about these entities, grounded in the artistic context of the lyrics.

- Steps -
1. **Entity Extraction**  
   Extract all named entities that match the **entity specification**, which can include:
   - A list of specific entity names (e.g., “Mưa”, “Người mẹ”, “Chiều”)
   - A list of general entity types (e.g., person, natural_element, object, space)

2. **Claim Extraction**  
   For each identified entity, extract all valid claims. Each claim must follow the structure below:

   - **Subject**: Name of the entity making or representing the symbolic or poetic action. Must be one of the extracted entities.
   - **Object**: Name of the entity affected by the claim or referenced by it. If unknown or symbolic, return **NONE**.
   - **Claim Type**: A reusable, capitalized label that categorizes the type of artistic relationship. Example values:  
     `SYMBOLIC_REFLECTION`, `EMOTIONAL_PROJECTION`, `TEMPORAL_COLLAPSE`, `GENDERED_REMEMBRANCE`, etc.
   - **Claim Status**: One of the following:
     - `TRUE`: The symbolic relationship is explicitly or strongly implied in the lyrics.
     - `FALSE`: The claim is contradicted or not supported.
     - `SUSPECTED`: The claim is interpretive or weakly implied.
   - **Claim Description**: A detailed explanation grounded in artistic reasoning.  
     Include references to applicable **artistic lenses** and **sublenses** (e.g., `nature_as_emotion_mirror`, `feminine_subjectivity`, `psychological_space`) and justify your interpretation with analysis.
   - **Claim Year**: A time period relevant to the symbolic claim in ISO-8601 format.  
     Format: `start_date`, `end_date`. If only one date is known, use it for both. If unknown, return **NONE**.
   - **Claim Source Text**: A list of all Vietnamese **lyric quotes** from the original text that directly support the claim.

Format each claim as (<subject_entity>{tuple_delimiter}<object_entity>{tuple_delimiter}<claim_type>{tuple_delimiter}<claim_status>{tuple_delimiter}<claim_start_date>{tuple_delimiter}<claim_end_date>{tuple_delimiter}<claim_description>{tuple_delimiter}<claim_source>)

3. **Output Formatting**  
- Return all claims as a single list, separated by **{record_delimiter}**
- End the output with **{completion_delimiter}**

- Additional Notes -
- Write all content in **English**, except for `claim_source`, Subject, Object quotes, which should remain in **Vietnamese**.
- Avoid speculation. All claims must be based on direct lyrics and/or symbolic relationships grounded in the artistic lenses provided.
- If a relationship is deeply embedded or metaphorical, clearly state the interpretive reasoning in the `claim_description`.

###############################
-Lăng kính nghệ thuật-
###############################
Below are the artistic lenses (sub-lenses) relevant to the analysis that must be referred to during entity extraction:

I. Lăng kính Thời gian
   1. Thời gian tuyến tính (Linear Time)
   2. Thời gian phi tuyến tính (Non-Linear Time)
   3. Thời gian vòng lặp (Cyclical Time)
   4. Thời gian tĩnh (Frozen Time)
   5. Thời gian vỡ vụn (Fragmented Time)
   6. Thời gian nghịch lý (Paradoxical Time)
   7. Thời gian mang tính tâm lý (Psychological Time)
   8. Thời gian mang tính biểu tượng (Symbolic Time)

II. Lăng kính Không gian
   1. Không gian địa lý (Geographical Space)
   2. Không gian biểu tượng (Symbolic Space)
   3. Không gian tâm lý (Psychological Space)
   4. Không gian thiên nhiên (Nature Space)
   5. Không gian siêu thực (Surreal Space)
   6. Không gian lịch sử (Historical Space)
   7. Không gian bị giới hạn và bức bối (Constrained Space)
   8. Không gian mở và tự do (Expansive Space)
   9. Không gian thiêng liêng (Sacred Space)
   10. Không gian phân mảnh (Fragmented Space)

III. Lăng kính Thiên nhiên
   1. Thiên nhiên như tấm gương nội tâm (Nature as Mirror of Emotion)
   2. Thiên nhiên như đối tượng siêu hình (Nature as a Metaphysical Entity)
   3. Thiên nhiên như biểu tượng luân hồi & vô thường (Nature as Impermanence)
   4. Thiên nhiên như hồi ức ký ức (Nature as Mnemonic Landscape)
   5. Thiên nhiên như biểu tượng quê hương & đất mẹ (Nature as Homeland)
   6. Thiên nhiên như nơi trú ngụ cuối cùng (Nature as Refuge or Return)

IV. Lăng kính Giới
   1. Nữ thể tính (Feminine Subjectivity)
   2. Cơ thể nữ tính (Feminine Body and Eroticism)
   3. Giới và chiến tranh (Gendered Experience of War)

V. Lăng kính Chủ nghĩa Phương Đông (Orientalism)
   1. Phong vị phương Đông trong thẩm mỹ (Eastern Aestheticism)
   2. Đông như là bản sắc đối lập Tây (East vs. West Identity)
   3. Tự nhiên và Đông phương luận (Nature and the East)
   4. Tâm linh và tính thiêng (Spiritual Orientalism)

VI. Lăng kính Existentialism
   1. Tha hóa con người trong xã hội sản xuất (Alienation from Capitalist Society)
   2. Công cụ hóa cơ thể – vật hóa con người (Reification and Objectification)
   3. Phê phán xã hội công nghiệp hóa (Critique of Industrialization and Modernity)
   4. Chiến tranh như sản phẩm của chủ nghĩa tư bản toàn cầu (War as Imperialist-Capitalist Structure)
   5. Cảm giác mất căn tính trong đô thị hóa – thị trường hóa (Identity Crisis under Urbanization and Market Logic)
   6. Kháng cự tiêu dùng & vật chất (Anti-consumerism & Spiritual Emptiness)

- Goal -
Given a text document (typically song lyrics), along with a predefined entity specification and claim criteria, extract:
1. All relevant entities that match the specification
2. All claims made between or about these entities, grounded in the artistic context of the lyrics.

- Steps -
1. **Entity Extraction**  
   Extract all named entities that match the **entity specification**, which can include:
   - A list of specific entity names (e.g., “Mưa”, “Người mẹ”, “Chiều”)
   - A list of general entity types (e.g., person, natural_element, object, space)

2. **Claim Extraction**  
   For each identified entity, extract all valid claims. Each claim must follow the structure below:

   - **Subject**: Name of the entity making or representing the symbolic or poetic action. Must be one of the extracted entities.
   - **Object**: Name of the entity affected by the claim or referenced by it. If unknown or symbolic, return **NONE**.
   - **Claim Type**: A reusable, capitalized label that categorizes the type of artistic relationship. Example values:  
     `SYMBOLIC_REFLECTION`, `EMOTIONAL_PROJECTION`, `TEMPORAL_COLLAPSE`, `GENDERED_REMEMBRANCE`, etc.
   - **Claim Status**: One of the following:
     - `TRUE`: The symbolic relationship is explicitly or strongly implied in the lyrics.
     - `FALSE`: The claim is contradicted or not supported.
     - `SUSPECTED`: The claim is interpretive or weakly implied.
   - **Claim Description**: A detailed explanation grounded in artistic reasoning.  
     Include references to applicable **artistic lenses** and **sublenses** (e.g., `nature_as_emotion_mirror`, `feminine_subjectivity`, `psychological_space`) and justify your interpretation with analysis.
   - **Claim Year**: A time period relevant to the symbolic claim in ISO-8601 format.  
     Format: `start_date`, `end_date`. If only one date is known, use it for both. If unknown, return **NONE**.
   - **Claim Source Text**: A list of all Vietnamese **lyric quotes** from the original text that directly support the claim.

Format each claim as (<subject_entity>{tuple_delimiter}<object_entity>{tuple_delimiter}<claim_type>{tuple_delimiter}<claim_status>{tuple_delimiter}<claim_start_date>{tuple_delimiter}<claim_end_date>{tuple_delimiter}<claim_description>{tuple_delimiter}<claim_source>)

3. **Output Formatting**  
- Return all claims as a single list, separated by **{record_delimiter}**
- End the output with **{completion_delimiter}**

- Additional Notes -
- Write all content in **English**, except for `claim_source`, Subject, Object quotes, which should remain in **Vietnamese**.
- Avoid speculation. All claims must be based on direct lyrics and/or symbolic relationships grounded in the artistic lenses provided.
- If a relationship is deeply embedded or metaphorical, clearly state the interpretive reasoning in the `claim_description`.
-Real Data-
Use the following input for your answer.
Entity specification: {entity_specs}
Claim description: {claim_description}
Song: {input_text}
Output:
"""


PROMPTS[
    "community_report"
] = """You are an AI assistant that helps a human analyst to generate thematic community reports based on artistic entities and their relationships extracted from the lyrics of Trịnh Công Sơn’s songs.

# GOAL
Given a list of interconnected artistic entities and relationships extracted from Trịnh Công Sơn’s lyrics (as a result of entity extraction + lens annotation), generate a **comprehensive Vietnamese-language community report** that summarizes the symbolic, emotional, philosophical, and cultural structure of that network.

The goal of this report is to **uncover the deeper artistic logic and interwoven meaning** within a community of motifs and images — for example: war-torn mothers, existential solitude, nature as impermanence, or feminine memory. The report will serve researchers and students analyzing Vietnamese song lyrics and identity formation.

# REPORT STRUCTURE
The report must be written in Vietnamese and follow this structure:

- **title**: Tên ngắn gọn, đại diện cho cộng đồng các thực thể đã cho. Ưu tiên dùng các hình ảnh hoặc thực thể nổi bật trong lời bài hát, ví dụ: `"Những xác người và ký ức chiến tranh"` hoặc `"Cơn mưa và những cõi đi về"`.

- **summary**: Một đoạn tóm tắt ngắn (~100-150 từ) mô tả cấu trúc biểu tượng của cộng đồng này: gồm những ai, những gì, mối quan hệ chủ đạo là gì, những lăng kính nào đang bao trùm (thời gian, không gian, thiên nhiên, giới, hiện sinh, v.v.).

- **impact_severity_rating**: Một số thực từ 0 đến 10 thể hiện **mức độ biểu tượng và ảnh hưởng tinh thần/nghệ thuật** mà cộng đồng này thể hiện trong không gian tư tưởng của Trịnh Công Sơn.

- **rating_explanation**: Một câu ngắn (~20-30 từ) giải thích tại sao cộng đồng này được đánh giá với chỉ số đó, dựa trên độ kết nối, chiều sâu biểu tượng, và sức nặng cảm xúc.

- **findings**: Một danh sách từ 5 đến 10 phát hiện quan trọng. Mỗi phát hiện gồm:
  - `summary`: Một câu tóm tắt phát hiện (dưới 20 từ).
  - `explanation`: Một đoạn dài (~1-3 đoạn văn), phân tích chuyên sâu về hiện tượng/chi tiết/biểu tượng dựa trên các thực thể và lăng kính nghệ thuật đã xác định trước.

# OUTPUT FORMAT
Return output as a **well-formed JSON** in the following structure:
    {{
      "title": <Tên tiêu đề báo cáo>,
      "summary": <Tóm tắt nội dung cộng đồng>,
      "rating": 8.5,
      "rating_explanation": "Cộng đồng mang chiều sâu biểu tượng và thể hiện rõ chủ đề hiện sinh và phản chiến.",
      "findings": [
        {{
          "summary": "Biểu tượng xác người và sự im lặng",
          "explanation": "Thực thể 'xác người', 'mẹ', và 'tiếng vỗ tay' cho thấy sự đảo chiều cảm xúc, kết hợp giữa đau thương và nghịch lý hiện sinh..."
        }},
        {{
          "summary": "Không gian chiến tranh và mất mát",
          "explanation": "Mối liên hệ giữa không gian 'bãi dâu', 'ngục tù', và 'người cha già' thể hiện không gian lịch sử và tâm lý bị tổn thương qua thời gian vỡ vụn..."
        }}
      ]
    }}
# GROUNDING RULES
- Các insight phải dựa trên **thực thể và quan hệ đã cho**, có **đối chiếu với lăng kính nghệ thuật cụ thể**.
- Không phát biểu suy đoán không có căn cứ trong dữ liệu đã trích xuất.
- Mỗi `explanation` cần thể hiện mối liên hệ giữa các chủ thể, hình ảnh và các chủ đề văn hóa – triết học – cảm xúc – nghệ thuật xuất hiện trong lời ca.

# DATA PROVIDED
You will be provided with:
- A list of entities (e.g., “Người mẹ”, “Mưa”, “Xác người”, “Chiều”, “Dòng sông”)
- A list of relationships (e.g., “Mẹ ru xác con”, “Chiều phủ lên xác người”)
- Each entity includes its lens annotations (e.g., ‘nature_as_emotion_mirror’, ‘feminine_subjectivity’, ‘war_as_capitalism’)
# Real Data

Use the following text for your answer. Do not make anything up in your answer.

Text:
```
{input_text}
```

Output:
"""

PROMPTS[
    "entity_extraction"
] = """-Goal-
Given a text document with song lyrics and a predefined set of artistic lenses (lăng kính nghệ thuật), identify all entities of the specified types and extract all meaningful relationships between these entities, while annotating them according to the sub-lenses listed in the "-Lăng kính nghệ thuật-" section below.

-Steps-
1. **Entity Extraction**  
   Identify all entities from the song lyrics (and context events if possible). Pay more attention and more attention on repeating words, themes and patterns. For each entity, extract the following:
   - `entity_name`: Capitalized name of the entity
   - `entity_type`: One of the following: [{entity_types}]
   - `entity_description`: A rich description including:
     - The entity’s role, attributes, or behavior in the lyrics
     - Its symbolic/artistic meaning in the context
     - Its corresponding artistic sub-lens (e.g., "Thời gian tĩnh", "Không gian thiêng liêng", "Nữ thể tính", etc.)

 Format each entity as:  
   ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. **Relationship Extraction**  
   Based on the entities above, identify all **clearly related** pairs. For each relationship:
   - `source_entity`: name of source entity
   - `target_entity`: name of target entity
   - `relationship_description`: explanation of how the entities are related within the song
   - `relationship_strength`: integer score from 1–10 indicating the strength of the relation

 Format each relationship as:  
   ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_strength>)

3. **Output Formatting**  
   - Return results in Vietnamese
   - Each record is separated by **{record_delimiter}**
   - End output with {completion_delimiter}


###############################
-Lăng kính nghệ thuật-
###############################
Below are the artistic lenses (sub-lenses) relevant to the analysis that must be referred to during entity extraction:

I. Lăng kính Existentialism
   1. Tha hóa con người trong xã hội sản xuất (Alienation from Capitalist Society)
   2. Công cụ hóa cơ thể – vật hóa con người (Reification and Objectification)
   3. Phê phán xã hội công nghiệp hóa (Critique of Industrialization and Modernity)
   4. Chiến tranh như sản phẩm của chủ nghĩa tư bản toàn cầu (War as Imperialist-Capitalist Structure)
   5. Cảm giác mất căn tính trong đô thị hóa – thị trường hóa (Identity Crisis under Urbanization and Market Logic)
   6. Kháng cự tiêu dùng & vật chất (Anti-consumerism & Spiritual Emptiness)

II. Lăng kính Không gian
   1. Không gian địa lý (Geographical Space)
   2. Không gian biểu tượng (Symbolic Space)
   3. Không gian tâm lý (Psychological Space)
   4. Không gian thiên nhiên (Nature Space)
   5. Không gian siêu thực (Surreal Space)
   6. Không gian lịch sử (Historical Space)
   7. Không gian bị giới hạn và bức bối (Constrained Space)
   8. Không gian mở và tự do (Expansive Space)
   9. Không gian thiêng liêng (Sacred Space)
   10. Không gian phân mảnh (Fragmented Space)

III. Lăng kính Thiên nhiên
   1. Thiên nhiên như tấm gương nội tâm (Nature as Mirror of Emotion)
   2. Thiên nhiên như đối tượng siêu hình (Nature as a Metaphysical Entity)
   3. Thiên nhiên như biểu tượng luân hồi & vô thường (Nature as Impermanence)
   4. Thiên nhiên như hồi ức ký ức (Nature as Mnemonic Landscape)
   5. Thiên nhiên như biểu tượng quê hương & đất mẹ (Nature as Homeland)
   6. Thiên nhiên như nơi trú ngụ cuối cùng (Nature as Refuge or Return)

IV. Lăng kính Thời gian
   1. Thời gian tuyến tính (Linear Time)
   2. Thời gian phi tuyến tính (Non-Linear Time)
   3. Thời gian vòng lặp (Cyclical Time)
   4. Thời gian tĩnh (Frozen Time)
   5. Thời gian vỡ vụn (Fragmented Time)
   6. Thời gian nghịch lý (Paradoxical Time)
   7. Thời gian mang tính tâm lý (Psychological Time)
   8. Thời gian mang tính biểu tượng (Symbolic Time)

V. Lăng kính Giới
   1. Nữ thể tính (Feminine Subjectivity)
   2. Cơ thể nữ tính (Feminine Body and Eroticism)
   3. Giới và chiến tranh (Gendered Experience of War)

VI. Lăng kính Chủ nghĩa Phương Đông (Orientalism)
   1. Phong vị phương Đông trong thẩm mỹ (Eastern Aestheticism)
   2. Đông như là bản sắc đối lập Tây (East vs. West Identity)
   3. Tự nhiên và Đông phương luận (Nature and the East)
   4. Tâm linh và tính thiêng (Spiritual Orientalism)

######################
-Examples-
######################
Example 1:
Text:
Mưa vẫn mưa bay trên tầng tháp cổ
Dài tay em mấy thuở mắt xanh xao
Nghe lá thu mưa reo mòn gót nhỏ
Đường dài hun hút cho mắt thêm sâu
################
Output:
################
("entity"{tuple_delimiter}"Mưa"{tuple_delimiter}"natural_element"{tuple_delimiter}"Hình ảnh mưa bay liên tục trong không gian cổ kính, phản ánh trạng thái cảm xúc buồn bã và mơ hồ. Gắn với sub-lens 'nature_as_emotion_mirror' và 'symbolic_time'."){record_delimiter}
("entity"{tuple_delimiter}"Tầng tháp cổ"{tuple_delimiter}"location"{tuple_delimiter}"Một địa điểm mang tính biểu tượng, gợi nhớ về không gian thiêng liêng và cổ kính. Gắn với sub-lens 'sacred_space'."){record_delimiter}
("entity"{tuple_delimiter}"Em"{tuple_delimiter}"person"{tuple_delimiter}"Nhân vật trữ tình nữ, gắn liền với hình ảnh mong manh, mơ hồ trong ký ức và thời gian. Gắn với 'feminine_subjectivity' và 'psychological_time'."){record_delimiter}
("entity"{tuple_delimiter}"Tay em"{tuple_delimiter}"body_part"{tuple_delimiter}"Đôi tay của nhân vật nữ, biểu tượng của sự yếu mềm và nhớ nhung trải dài qua thời gian. Gắn với 'feminine_body' và 'nonlinear_time'."){record_delimiter}
("entity"{tuple_delimiter}"Mắt xanh xao"{tuple_delimiter}"body_part"{tuple_delimiter}"Đôi mắt gợi sự buồn bã, hoài niệm, mang tính biểu tượng cho nội tâm mong manh. Gắn với 'feminine_body' và 'psychological_space'."){record_delimiter}
("entity"{tuple_delimiter}"Lá thu"{tuple_delimiter}"natural_element"{tuple_delimiter}"Chiếc lá mùa thu gợi cảm giác trôi qua, tàn lụi. Gắn với 'nature_as_impermanence'."){record_delimiter}
("entity"{tuple_delimiter}"Gót nhỏ"{tuple_delimiter}"body_part"{tuple_delimiter}"Bước chân nhẹ, gợi hình ảnh nữ tính, mòn mỏi trên con đường đời. Gắn với 'feminine_body' và 'psychological_time'."){record_delimiter}
("entity"{tuple_delimiter}"Đường dài hun hút"{tuple_delimiter}"location"{tuple_delimiter}"Không gian kéo dài vô định, gợi sự trống trải và mất phương hướng. Gắn với 'expansive_space' và 'fragmented_space'."){record_delimiter}

("relationship"{tuple_delimiter}"Mưa"{tuple_delimiter}"Tầng tháp cổ"{tuple_delimiter}"Mưa bay trên tầng tháp cổ tạo nên không gian thiêng liêng và hoài niệm, vừa thực vừa siêu thực."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Em"{tuple_delimiter}"Tay em"{tuple_delimiter}"Đôi tay là một phần của nhân vật Em, biểu hiện sự kéo dài của nỗi nhớ."{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Em"{tuple_delimiter}"Mắt xanh xao"{tuple_delimiter}"Mắt xanh xao thể hiện trạng thái nội tâm yếu mềm và u sầu của Em."{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Lá thu"{tuple_delimiter}"Mưa"{tuple_delimiter}"Lá thu và mưa cùng nhau tạo nên bức tranh mùa thu buồn, tượng trưng cho sự vô thường."{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Gót nhỏ"{tuple_delimiter}"Đường dài hun hút"{tuple_delimiter}"Bước chân nhỏ mòn mỏi trên con đường dài gợi cảm giác lạc lõng, phản ánh thời gian phi tuyến tính và tâm lý."{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Mắt xanh xao"{tuple_delimiter}"Đường dài hun hút"{tuple_delimiter}"Cái nhìn sâu thẳm hướng vào không gian vô định, thể hiện cảm giác cô đơn và mất mát."{tuple_delimiter}9){completion_delimiter}


   
#############################
-Real Data-
#############################
Use the following input for your answer.

Text: {input_text}

Output:
"""


PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""


PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["concept", "person", "geo", "nature", "event", "artistic symbols", "religious", "spiritual", "space", "time", "beauty", "war", "love", "family", "organization", "other symbols"]
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS[
    "local_rag_response"
] = """--- Vai trò ---

Bạn là một trợ lý AI chuyên phân tích biểu tượng và hình ảnh nghệ thuật trong lời bài hát Trịnh Công Sơn.  
Bạn có nhiệm vụ trả lời các câu hỏi mang tính phân tích, khám phá ý nghĩa biểu tượng của một hình ảnh cụ thể (ví dụ: mưa, người mẹ, chiều, dòng sông...) bằng cách rút ra những điểm then chốt từ các bảng dữ liệu được cung cấp.

--- Mục tiêu ---

Hãy tạo một phản hồi có độ dài và định dạng đúng như yêu cầu tại {response_type}, nhằm:
- Trả lời đúng và đầy đủ câu hỏi của người dùng
- Tổng hợp các báo cáo phân tích từ nhiều cluster khác nhau (các cluster này có thể đã tập trung vào những khía cạnh hoặc bài hát khác nhau). Tuy nhiên, cần dọn sạch định dạng, các nguồn của cluster (VD: Report 0,...) trong cầu trả lời cuối cùng
- Tập trung vào trích dẫn cụ thể từ lời bài nhạc với tên bài nhạc tương ứng
- Giữ nguyên thứ tự quan trọng: **các báo cáo được sắp xếp theo thứ tự giảm dần về độ quan trọng**

Nếu không có đủ thông tin để trả lời câu hỏi, hãy nói rõ điều đó. Tuyệt đối **không suy đoán hoặc bịa đặt nội dung**.

--- Cách thực hiện ---

1. **Loại bỏ** mọi thông tin không liên quan
2. **Hợp nhất** thông tin cốt lõi từ các báo cáo vào một nội dung nhất quán, liền mạch
3. **Giải thích rõ** các điểm quan trọng và ý nghĩa tiềm ẩn (biểu tượng, lăng kính nghệ thuật, văn cảnh...)
4. **Trích dẫn** đầy đủ chính xác từ thông tin và lời các bài hát kèm theo thời gian sáng tác
4. **Chia thành các đoạn, phần hợp lý**, có thể đặt tiêu đề nếu nội dung dài
5. **Định dạng kết quả bằng Markdown**, thích hợp cho người đọc tiếng Việt và có nền tảng văn hóa – học thuật

--- Nguyên tắc trình bày ---

- Tránh lập lại máy móc
- Viết bằng văn phong học thuật, súc tích, rõ ràng
- Giữ nguyên các động từ mang tính mô thức như “sẽ”, “có thể”, “nên” khi xuất hiện trong nội dung gốc
- Tuyệt đối **không thêm bất kỳ thông tin nào không có bằng chứng rõ ràng từ các báo cáo**

---Độ dài và định dạng mục tiêu---

{response_type}


---Dữ Lệu được cho ---

{context_data}


--- Mục tiêu ---

Hãy tạo một phản hồi có độ dài và định dạng đúng như yêu cầu tại mục Độ dài và định dạng mục tiêu, nhằm:
- Trả lời đúng và đầy đủ câu hỏi của người dùng
- Tổng hợp các báo cáo phân tích từ nhiều chuyên gia khác nhau (các chuyên gia này có thể đã tập trung vào những khía cạnh hoặc bài hát khác nhau)
- Giữ nguyên thứ tự quan trọng: **các báo cáo được sắp xếp theo thứ tự giảm dần về độ quan trọng**

Nếu không có đủ thông tin để trả lời câu hỏi, hãy nói rõ điều đó. Tuyệt đối **không suy đoán hoặc bịa đặt nội dung**.


---Độ dài và định dạng mục tiêu---

{response_type}


"""

PROMPTS[
    "global_map_rag_points"
] = """--- Vai trò ---

Bạn là một trợ lý AI chuyên phân tích biểu tượng và hình ảnh nghệ thuật trong lời bài hát Trịnh Công Sơn.  
Bạn có nhiệm vụ trả lời các câu hỏi mang tính phân tích, khám phá ý nghĩa biểu tượng của một hình ảnh cụ thể (ví dụ: mưa, người mẹ, chiều, dòng sông...) bằng cách rút ra những điểm then chốt từ các bảng dữ liệu được cung cấp.

--- Mục tiêu ---

Hãy tạo một phản hồi ở dạng JSON bao gồm một danh sách các **key points** liên quan đến câu hỏi của người dùng. Mỗi key point phải:
- Tổng hợp thông tin từ bảng dữ liệu đầu vào
- Tập trung vào **các khía cạnh biểu tượng, cảm xúc, triết học hoặc ngữ cảnh nghệ thuật** của hình ảnh trong các bài hát Trịnh Công Sơn
- Trình bày ngắn gọn nhưng rõ ràng về ý nghĩa và chức năng của hình ảnh đó trong lời nhạc

Nếu bảng dữ liệu không đủ thông tin để đưa ra câu trả lời, hãy ghi rõ điều đó trong một điểm duy nhất với `score = 0`.

--- Định dạng phản hồi (JSON) ---

```json
{{
  "points": [
    {{
      "description": "Mô tả đầy đủ và mạch lạc của điểm phân tích thứ nhất về hình ảnh hoặc biểu tượng.",
      "score": score_value (số nguyên từ 0 đến 100 thể hiện tầm quan trọng của điểm này trong việc trả lời câu hỏi)
    }},
    {{
      "description": "Mô tả điểm phân tích tiếp theo...",
      "score": score_value
    }}
  ]
}}
--- Nguyên tắc trình bày ---

Không suy đoán. Chỉ sử dụng thông tin có trong dữ liệu đầu vào {context_data}.

Nếu có thể, hãy liên kết mô tả với các lăng kính nghệ thuật đã được xác định như thời gian phi tuyến, thiên nhiên như tấm gương nội tâm, giới và chiến tranh, không gian thiêng liêng, v.v.

Tôn trọng ngữ nghĩa gốc, bao gồm các modal verbs như “sẽ”, “có thể”, “nên” nếu có trong dữ liệu.

Ưu tiên giữ nguyên các trích dẫn lời bài hát nếu xuất hiện.
Trả lời phải dành cho độc giả người Việt, sử dụng văn phong học thuật, súc tích, dễ hiểu.

--- Dữ liệu phân tích ---
{context_data}

--- Mục tiêu ---

Hãy tạo một phản hồi ở dạng JSON bao gồm một danh sách các **key points** liên quan đến câu hỏi của người dùng. Mỗi key point phải:
- Tổng hợp thông tin từ bảng dữ liệu đầu vào
- Tập trung vào **các khía cạnh biểu tượng, cảm xúc, triết học hoặc ngữ cảnh nghệ thuật** của hình ảnh trong các bài hát Trịnh Công Sơn
- Trình bày ngắn gọn nhưng rõ ràng về ý nghĩa và chức năng của hình ảnh đó trong lời nhạc

Nếu bảng dữ liệu không đủ thông tin để đưa ra câu trả lời, hãy ghi rõ điều đó trong một điểm duy nhất với `score = 0`.

--- Định dạng phản hồi (JSON) ---

```json
{{
  "points": [
    {{
      "description": "Mô tả đầy đủ và mạch lạc của điểm phân tích thứ nhất về hình ảnh hoặc biểu tượng.",
      "score": score_value (số nguyên từ 0 đến 100 thể hiện tầm quan trọng của điểm này trong việc trả lời câu hỏi)
    }},
    {{
      "description": "Mô tả điểm phân tích tiếp theo...",
      "score": score_value
    }}
  ]
}}
--- Nguyên tắc trình bày ---

Không suy đoán. Chỉ sử dụng thông tin có trong dữ liệu đầu vào {context_data}.

Nếu có thể, hãy liên kết mô tả với các lăng kính nghệ thuật đã được xác định như thời gian phi tuyến, thiên nhiên như tấm gương nội tâm, giới và chiến tranh, không gian thiêng liêng, v.v.

Tôn trọng ngữ nghĩa gốc, bao gồm các modal verbs như “sẽ”, “có thể”, “nên” nếu có trong dữ liệu.

Ưu tiên giữ nguyên các trích dẫn lời bài hát nếu xuất hiện.
Trả lời phải dành cho độc giả người Việt, sử dụng văn phong học thuật, súc tích, dễ hiểu.

--- Dữ liệu phân tích ---
{context_data}

"""

PROMPTS[
    "global_reduce_rag_response"
] = """
--- Vai trò ---

Bạn là một trợ lý AI am hiểu văn hóa, có nhiệm vụ tổng hợp và diễn giải lại các báo cáo phân tích của nhiều chuyên gia về lời bài hát Trịnh Công Sơn, nhằm trả lời một câu hỏi cụ thể từ người dùng.

--- Mục tiêu ---

Hãy tạo một phản hồi có độ dài và định dạng đúng như yêu cầu tại {response_type}, nhằm:
- Trả lời đúng và đầy đủ câu hỏi của người dùng
- Tổng hợp các báo cáo phân tích từ nhiều chuyên gia khác nhau (các chuyên gia này có thể đã tập trung vào những khía cạnh hoặc bài hát khác nhau)
- Giữ nguyên thứ tự quan trọng: **các báo cáo được sắp xếp theo thứ tự giảm dần về độ quan trọng**

Nếu không có đủ thông tin để trả lời câu hỏi, hãy nói rõ điều đó. Tuyệt đối **không suy đoán hoặc bịa đặt nội dung**.

--- Cách thực hiện ---

1. **Loại bỏ** mọi thông tin không liên quan
2. **Hợp nhất** thông tin cốt lõi từ các báo cáo vào một nội dung nhất quán, liền mạch
3. **Giải thích rõ** các điểm quan trọng và ý nghĩa tiềm ẩn (biểu tượng, lăng kính nghệ thuật, văn cảnh...)
4. **Chia thành các đoạn, phần hợp lý**, có thể đặt tiêu đề nếu nội dung dài
5. **Định dạng kết quả bằng Markdown**, thích hợp cho người đọc tiếng Việt và có nền tảng văn hóa – học thuật

--- Nguyên tắc trình bày ---

- Tránh lập lại máy móc
- Viết bằng văn phong học thuật, súc tích, rõ ràng
- Giữ nguyên các động từ mang tính mô thức như “sẽ”, “có thể”, “nên” khi xuất hiện trong nội dung gốc
- Tuyệt đối **không thêm bất kỳ thông tin nào không có bằng chứng rõ ràng từ các báo cáo**

--- Định dạng đầu ra mong muốn ---

{response_type}

--- Dữ liệu phân tích ---

{report_data}

--- Mục tiêu ---

Hãy tạo một phản hồi có độ dài và định dạng đúng như yêu cầu tại {response_type}, nhằm:
- Trả lời đúng và đầy đủ câu hỏi của người dùng
- Tổng hợp các báo cáo phân tích từ nhiều chuyên gia khác nhau (các chuyên gia này có thể đã tập trung vào những khía cạnh hoặc bài hát khác nhau)
- Giữ nguyên thứ tự quan trọng: **các báo cáo được sắp xếp theo thứ tự giảm dần về độ quan trọng**

Nếu không có đủ thông tin để trả lời câu hỏi, hãy nói rõ điều đó. Tuyệt đối **không suy đoán hoặc bịa đặt nội dung**.

--- Cách thực hiện ---

1. **Loại bỏ** mọi thông tin không liên quan
2. **Hợp nhất** thông tin cốt lõi từ các báo cáo vào một nội dung nhất quán, liền mạch
3. **Giải thích rõ** các điểm quan trọng và ý nghĩa tiềm ẩn (biểu tượng, lăng kính nghệ thuật, văn cảnh...)
4. **Chia thành các đoạn, phần hợp lý**, có thể đặt tiêu đề nếu nội dung dài
5. **Định dạng kết quả bằng Markdown**, thích hợp cho người đọc tiếng Việt và có nền tảng văn hóa – học thuật

--- Nguyên tắc trình bày ---

- Tránh lập lại máy móc
- Viết bằng văn phong học thuật, súc tích, rõ ràng
- Giữ nguyên các động từ mang tính mô thức như “sẽ”, “có thể”, “nên” khi xuất hiện trong nội dung gốc
- Tuyệt đối **không thêm bất kỳ thông tin nào không có bằng chứng rõ ràng từ các báo cáo**

--- Định dạng đầu ra mong muốn ---

{response_type}

--- Dữ liệu phân tích ---

{report_data}
"""

PROMPTS[
    "naive_rag_response"
] = """You're a helpful assistant
--- Dữ liệu bạn có thể sử dụng ---
{content_data}
---

Bạn là một trợ lý AI có nhiệm vụ trả lời câu hỏi của người dùng dựa trên các thông tin đã cung cấp phía trên. Nội dung tập trung vào việc phân tích nghệ thuật, biểu tượng và lăng kính trong lời bài hát Trịnh Công Sơn.

Nếu bạn **không tìm thấy đủ thông tin** để đưa ra câu trả lời phù hợp trong phần dữ liệu trên, **hãy nói rõ rằng bạn không thể trả lời**, và **không được tự suy đoán hoặc bịa ra thông tin**.

Hãy tạo một phản hồi có độ dài và định dạng theo yêu cầu tại phần `{response_type}`, đáp ứng đúng câu hỏi của người dùng bằng cách:
- Tóm tắt và tổng hợp toàn bộ thông tin từ phần dữ liệu đầu vào
- Diễn giải rõ ràng, mạch lạc và sâu sắc
- Có thể bổ sung kiến thức nền liên quan đến **nghệ thuật, văn học, triết học hoặc lịch sử Việt Nam**, nhưng chỉ khi phù hợp và cần thiết cho việc hiểu đúng lời bài hát

Không bao gồm thông tin không có căn cứ hoặc không hiện diện trong dữ liệu đã cho.

--- Định dạng và độ dài phản hồi yêu cầu ---
{response_type}
"""

PROMPTS["fail_response"] = "Xin lỗi, tôi không thể trả lời được câu hỏi này :'("

PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["default_text_separator"] = [
    # Paragraph separators
    "\n\n",
    "\r\n\r\n",
    # Line breaks
    "\n",
    "\r\n",
    # Sentence ending punctuation
    "。",  # Chinese period
    "．",  # Full-width dot
    ".",  # English period
    "！",  # Chinese exclamation mark
    "!",  # English exclamation mark
    "？",  # Chinese question mark
    "?",  # English question mark
    # Whitespace characters
    " ",  # Space
    "\t",  # Tab
    "\u3000",  # Full-width space
    # Special characters
    "\u200b",  # Zero-width space (used in some Asian languages)
]
