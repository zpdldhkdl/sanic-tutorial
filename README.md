### API Spec

| HTTP Method | Path                          | Description    |
| ----------- | ----------------------------- | -------------- |
| GET         | /todo/tasks                   | 테스크 전체 조회  |
| POST        | /todo/tasks                   | 테스크 생성      |
| GET         | /todo/tasks/{task_id}         | 테스크 조회      |
| DELETE      | /todo/tasks/{task_id}         | 테스크 삭제      |
| PUT         | /todo/tasks/{task_id}         | 테스크 수정      |

### Create Table SQL

```sql
CREATE TABLE `schema_name`.`table_name` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `status` TINYINT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);
```
