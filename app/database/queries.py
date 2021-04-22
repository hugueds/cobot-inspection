# SELECT P.Name PROCESS,F.NAME FUNC, S.NAME STATION, W.NAME POSITION, T.CONTRACTID CIMI, E.CUOBJ CU, E.POPID, T.TOO, T.OBJ, T.QUANTITY, T.SNAME, W.DESCRIPTION, WCS.Name ESTRUTURA
#        FROM 
#        [LTS].[dbo].[EWO_TASKROW] T, 
#        [LTS].[dbo].[EWO] E, 
# 	   [LTS].[dbo].[TB_PROCESS] P, 
#        [LTS].[dbo].[TB_STATION] S, 
#        [LTS].[dbo].[TB_FUNCTION] F, 
#        [LTS].[dbo].[TB_WORKPLACE] W, 
#        [LTS].[dbo].[TB_WORKPLACE_CIMI] WC, 
#        [LTS].[dbo].[TB_WORKPLACE_STRUCTURE] WCS
#        WHERE   1 = 1
#         AND T.IPOID = E.IPOID                     
#         AND T.CONTRACTID = E.CONTRACTID		   
# 		AND F.ID_PROCESS = P.Id 
#         AND S.ID = W.ID_STATION                   
#         AND S.ID_FUNCTION = F.ID                  
#         AND WC.IdWorkplace = W.ID                 
#         AND WC.CIMI =  T.CONTRACTID         
#         AND WCS.Id = WC.IdStructure                        		 
# 		AND TOO = 'LT'        
# 		AND P.Name = 'ML1'
# 		AND S.NAME = ''
# 		AND W.NAME = ''
# 		AND E.POPID = '602761'		 		 
		 
#          ORDER BY F.POSITION, S.POSITION, W.POSITION, T.LINENUM
		 
