https://docs.djangoproject.com/zh-hans/5.0/intro/tutorial01/
https://www.bilibili.com/video/BV1cm4y127ce?p=38&spm_id_from=pageDriver&vd_source=4825f093b332088b99207eb66ec67b90

<!--https://github.com/liuly0322/teacher-management-system/tree/main?tab=readme-ov-file-->
https://v4.bootcss.com/docs/getting-started/introduction/
https://www.cnblogs.com/tuyin/p/17142353.html#_label15

## 连接MYSQL
- 安装mysqlclient
  ```shell
    pip install mysqlclient
  ```

- 启动MySQL
  ```
   mysql.server start
  ```


## 创建数据表
### 教师表
```mermaid
erDiagram
    TEACHER {
        char(5) ID PK
        char(256) name
        int sex "2 values available"
        int position "11 values available"
    }
```
### 论文表
```mermaid
erDiagram
    PAPER {
        int ID PK
        char(256) title
        char(256) source
        date publish_date
        int publish_type
        int publish_level 
    }
```
#### 教师-论文中间表
一篇论文必须至少一名作者。而一个教师不一定发表过论文。
```mermaid
erDiagram
  TEACHER ||--o{ TEACHER_PAPER : has
    PAPER ||--|{ TEACHER_PAPER : has
    TEACHER_PAPER {
        char(5) teacher_id PK,FK
        int paper_id PK,FK
        int rank
        bool is_corresponding_author
    }
```
### 项目表
```mermaid
erDiagram
    PROJECT {
        char(256) ID PK
        char(256) name
        char(256) source
        int type
        float fund
        date start_date
        date end_date "nullable"
    }
```
#### 教师_项目中间表
```mermaid
erDiagram
  TEACHER ||--o{ TEACHER_PROJECT : has
    PROJECT ||--|{ TEACHER_PROJECT : has
    TEACHER_PROJECT {
        char(5) teacher_id PK,FK
        char(256) project_id PK,FK
        int rank
        float fund_taken
    }
```
### 课程表
```mermaid
erDiagram
    COURSE {
        char(256) ID PK
        char(256) name
        int hours
        int type
    }
```
#### 教师-课程中间表
```mermaid
erDiagram
  TEACHER ||--o{ TEACHER_COURSE : has
    COURSE ||--|{ TEACHER_COURSE : has
    TEACHER_COURSE {
        char(5) teacher_id PK,FK
        char(256) course_id PK,FK
        int year
        int semester
        int hours_taken
    }
```

