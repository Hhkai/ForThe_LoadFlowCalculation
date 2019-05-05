# ForThe_LoadFlowCalculation
## djk:
两个文本形式的输出文件
- out.dis
> 每行对应LF.L1的行, 由近到远排列了所有发电机 ``<发电机在LF.L1的行号>:<距离>, ...''
- nameout.dis
> 方便在小规模图上的简单检查, 把out.dis里的行号替换为了母线名, 并省去了距离
