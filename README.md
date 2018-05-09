### 端口监控，TCP SYN 状态监控，TCP ESTABLISH 状态监控

### 当前版本：2.0.1

### 当前路径下文件名对应源文件名称
  * 如果当前环境不能执行已有的 BIN 文件，请复制系统中默认的文件到当前路径下
  - find_string: egrep
  - scan_listen_port: ss

### 运行方式
  - ./port_diff.py
  - python2.7 ./port_diff.py

### 用法
  - Usage: ./port_diff.py port_diff|tcp_syn_check|tcp_estab_check
  - ./port_diff.py port_diff       # 端口监控，减少端口或者增加端口会出现告警
  - ./port_diff.py tcp_syn_check   # TCP SYN 状态连接数
  - ./port_diff.py tcp_estab_check # TCP ESTABLISH 状态连接数

### 说明
  * cache 目录需要手动创建且注意权限问题

### 表示当前系统正常
  - port_diff => output: OK
  - tcp_syn_check|tcp_estab_check 返回当前状态值

### ChangeLog
  - 2.0.1
    listen.db 错误告警而不是异常导致 zabbix 出现不支持 item key

  - 2.0.0
    tcp syn, tcp estab 状态输出监控值而不是在脚本进行监控是否告警
