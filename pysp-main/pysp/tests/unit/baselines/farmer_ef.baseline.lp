\* Source Pyomo model name=MASTER *\

min 
MASTER:
+76.666665899999998 AboveAverageScenario_DevotedAcreage(CORN)
+86.66666579999999 AboveAverageScenario_DevotedAcreage(SUGAR_BEETS)
+49.999999499999994 AboveAverageScenario_DevotedAcreage(WHEAT)
+69.999999299999999 AboveAverageScenario_QuantityPurchased(CORN)
+33333.332999999999 AboveAverageScenario_QuantityPurchased(SUGAR_BEETS)
+79.333332540000001 AboveAverageScenario_QuantityPurchased(WHEAT)
-49.999999499999994 AboveAverageScenario_QuantitySubQuotaSold(CORN)
-11.999999879999999 AboveAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
-56.6666661 AboveAverageScenario_QuantitySubQuotaSold(WHEAT)
-3.3333332999999996 AboveAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
+76.666668199999989 AverageScenario_DevotedAcreage(CORN)
+86.666668399999992 AverageScenario_DevotedAcreage(SUGAR_BEETS)
+50.000000999999997 AverageScenario_DevotedAcreage(WHEAT)
+70.000001400000002 AverageScenario_QuantityPurchased(CORN)
+33333.333999999995 AverageScenario_QuantityPurchased(SUGAR_BEETS)
+79.333334919999999 AverageScenario_QuantityPurchased(WHEAT)
-50.000000999999997 AverageScenario_QuantitySubQuotaSold(CORN)
-12.000000239999999 AverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
-56.666667799999999 AverageScenario_QuantitySubQuotaSold(WHEAT)
-3.3333333999999999 AverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
+76.666665899999998 BelowAverageScenario_DevotedAcreage(CORN)
+86.66666579999999 BelowAverageScenario_DevotedAcreage(SUGAR_BEETS)
+49.999999499999994 BelowAverageScenario_DevotedAcreage(WHEAT)
+69.999999299999999 BelowAverageScenario_QuantityPurchased(CORN)
+33333.332999999999 BelowAverageScenario_QuantityPurchased(SUGAR_BEETS)
+79.333332540000001 BelowAverageScenario_QuantityPurchased(WHEAT)
-49.999999499999994 BelowAverageScenario_QuantitySubQuotaSold(CORN)
-11.999999879999999 BelowAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
-56.6666661 BelowAverageScenario_QuantitySubQuotaSold(WHEAT)
-3.3333332999999996 BelowAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)

s.t.

c_e_MASTER_BLEND_CONSTRAINT_RootNode(1)_:
-1 BelowAverageScenario_DevotedAcreage(CORN)
+1 MASTER_BLEND_VAR_RootNode(_DevotedAcreage__CORN_)
= 0

c_e_MASTER_BLEND_CONSTRAINT_RootNode(2)_:
-1 AverageScenario_DevotedAcreage(CORN)
+1 MASTER_BLEND_VAR_RootNode(_DevotedAcreage__CORN_)
= 0

c_e_MASTER_BLEND_CONSTRAINT_RootNode(3)_:
-1 AboveAverageScenario_DevotedAcreage(CORN)
+1 MASTER_BLEND_VAR_RootNode(_DevotedAcreage__CORN_)
= 0

c_e_MASTER_BLEND_CONSTRAINT_RootNode(4)_:
-1 BelowAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1 MASTER_BLEND_VAR_RootNode(_DevotedAcreage__SUGAR_BEETS_)
= 0

c_e_MASTER_BLEND_CONSTRAINT_RootNode(5)_:
-1 AverageScenario_DevotedAcreage(SUGAR_BEETS)
+1 MASTER_BLEND_VAR_RootNode(_DevotedAcreage__SUGAR_BEETS_)
= 0

c_e_MASTER_BLEND_CONSTRAINT_RootNode(6)_:
-1 AboveAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1 MASTER_BLEND_VAR_RootNode(_DevotedAcreage__SUGAR_BEETS_)
= 0

c_e_MASTER_BLEND_CONSTRAINT_RootNode(7)_:
-1 BelowAverageScenario_DevotedAcreage(WHEAT)
+1 MASTER_BLEND_VAR_RootNode(_DevotedAcreage__WHEAT_)
= 0

c_e_MASTER_BLEND_CONSTRAINT_RootNode(8)_:
-1 AverageScenario_DevotedAcreage(WHEAT)
+1 MASTER_BLEND_VAR_RootNode(_DevotedAcreage__WHEAT_)
= 0

c_e_MASTER_BLEND_CONSTRAINT_RootNode(9)_:
-1 AboveAverageScenario_DevotedAcreage(WHEAT)
+1 MASTER_BLEND_VAR_RootNode(_DevotedAcreage__WHEAT_)
= 0

c_u_BelowAverageScenario_ConstrainTotalAcreage_:
+1 BelowAverageScenario_DevotedAcreage(CORN)
+1 BelowAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1 BelowAverageScenario_DevotedAcreage(WHEAT)
<= 500

c_l_BelowAverageScenario_EnforceCattleFeedRequirement(CORN)_:
+2.3999999999999999 BelowAverageScenario_DevotedAcreage(CORN)
+1 BelowAverageScenario_QuantityPurchased(CORN)
-1 BelowAverageScenario_QuantitySubQuotaSold(CORN)
-1 BelowAverageScenario_QuantitySuperQuotaSold(CORN)
>= 240

c_l_BelowAverageScenario_EnforceCattleFeedRequirement(SUGAR_BEETS)_:
+16 BelowAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1 BelowAverageScenario_QuantityPurchased(SUGAR_BEETS)
-1 BelowAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
-1 BelowAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
>= 0

c_l_BelowAverageScenario_EnforceCattleFeedRequirement(WHEAT)_:
+2 BelowAverageScenario_DevotedAcreage(WHEAT)
+1 BelowAverageScenario_QuantityPurchased(WHEAT)
-1 BelowAverageScenario_QuantitySubQuotaSold(WHEAT)
-1 BelowAverageScenario_QuantitySuperQuotaSold(WHEAT)
>= 200

c_u_BelowAverageScenario_LimitAmountSold(CORN)_:
-2.3999999999999999 BelowAverageScenario_DevotedAcreage(CORN)
+1 BelowAverageScenario_QuantitySubQuotaSold(CORN)
+1 BelowAverageScenario_QuantitySuperQuotaSold(CORN)
<= 0

c_u_BelowAverageScenario_LimitAmountSold(SUGAR_BEETS)_:
-16 BelowAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1 BelowAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
+1 BelowAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
<= 0

c_u_BelowAverageScenario_LimitAmountSold(WHEAT)_:
-2 BelowAverageScenario_DevotedAcreage(WHEAT)
+1 BelowAverageScenario_QuantitySubQuotaSold(WHEAT)
+1 BelowAverageScenario_QuantitySuperQuotaSold(WHEAT)
<= 0

r_l_BelowAverageScenario_EnforceQuotas(CORN)_:
+1 BelowAverageScenario_QuantitySubQuotaSold(CORN)
>= 0

r_u_BelowAverageScenario_EnforceQuotas(CORN)_:
+1 BelowAverageScenario_QuantitySubQuotaSold(CORN)
<= 100000

r_l_BelowAverageScenario_EnforceQuotas(SUGAR_BEETS)_:
+1 BelowAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
>= 0

r_u_BelowAverageScenario_EnforceQuotas(SUGAR_BEETS)_:
+1 BelowAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
<= 6000

r_l_BelowAverageScenario_EnforceQuotas(WHEAT)_:
+1 BelowAverageScenario_QuantitySubQuotaSold(WHEAT)
>= 0

r_u_BelowAverageScenario_EnforceQuotas(WHEAT)_:
+1 BelowAverageScenario_QuantitySubQuotaSold(WHEAT)
<= 100000

c_u_AverageScenario_ConstrainTotalAcreage_:
+1 AverageScenario_DevotedAcreage(CORN)
+1 AverageScenario_DevotedAcreage(SUGAR_BEETS)
+1 AverageScenario_DevotedAcreage(WHEAT)
<= 500

c_l_AverageScenario_EnforceCattleFeedRequirement(CORN)_:
+3 AverageScenario_DevotedAcreage(CORN)
+1 AverageScenario_QuantityPurchased(CORN)
-1 AverageScenario_QuantitySubQuotaSold(CORN)
-1 AverageScenario_QuantitySuperQuotaSold(CORN)
>= 240

c_l_AverageScenario_EnforceCattleFeedRequirement(SUGAR_BEETS)_:
+20 AverageScenario_DevotedAcreage(SUGAR_BEETS)
+1 AverageScenario_QuantityPurchased(SUGAR_BEETS)
-1 AverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
-1 AverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
>= 0

c_l_AverageScenario_EnforceCattleFeedRequirement(WHEAT)_:
+2.5 AverageScenario_DevotedAcreage(WHEAT)
+1 AverageScenario_QuantityPurchased(WHEAT)
-1 AverageScenario_QuantitySubQuotaSold(WHEAT)
-1 AverageScenario_QuantitySuperQuotaSold(WHEAT)
>= 200

c_u_AverageScenario_LimitAmountSold(CORN)_:
-3 AverageScenario_DevotedAcreage(CORN)
+1 AverageScenario_QuantitySubQuotaSold(CORN)
+1 AverageScenario_QuantitySuperQuotaSold(CORN)
<= 0

c_u_AverageScenario_LimitAmountSold(SUGAR_BEETS)_:
-20 AverageScenario_DevotedAcreage(SUGAR_BEETS)
+1 AverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
+1 AverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
<= 0

c_u_AverageScenario_LimitAmountSold(WHEAT)_:
-2.5 AverageScenario_DevotedAcreage(WHEAT)
+1 AverageScenario_QuantitySubQuotaSold(WHEAT)
+1 AverageScenario_QuantitySuperQuotaSold(WHEAT)
<= 0

r_l_AverageScenario_EnforceQuotas(CORN)_:
+1 AverageScenario_QuantitySubQuotaSold(CORN)
>= 0

r_u_AverageScenario_EnforceQuotas(CORN)_:
+1 AverageScenario_QuantitySubQuotaSold(CORN)
<= 100000

r_l_AverageScenario_EnforceQuotas(SUGAR_BEETS)_:
+1 AverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
>= 0

r_u_AverageScenario_EnforceQuotas(SUGAR_BEETS)_:
+1 AverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
<= 6000

r_l_AverageScenario_EnforceQuotas(WHEAT)_:
+1 AverageScenario_QuantitySubQuotaSold(WHEAT)
>= 0

r_u_AverageScenario_EnforceQuotas(WHEAT)_:
+1 AverageScenario_QuantitySubQuotaSold(WHEAT)
<= 100000

c_u_AboveAverageScenario_ConstrainTotalAcreage_:
+1 AboveAverageScenario_DevotedAcreage(CORN)
+1 AboveAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1 AboveAverageScenario_DevotedAcreage(WHEAT)
<= 500

c_l_AboveAverageScenario_EnforceCattleFeedRequirement(CORN)_:
+3.6000000000000001 AboveAverageScenario_DevotedAcreage(CORN)
+1 AboveAverageScenario_QuantityPurchased(CORN)
-1 AboveAverageScenario_QuantitySubQuotaSold(CORN)
-1 AboveAverageScenario_QuantitySuperQuotaSold(CORN)
>= 240

c_l_AboveAverageScenario_EnforceCattleFeedRequirement(SUGAR_BEETS)_:
+24 AboveAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1 AboveAverageScenario_QuantityPurchased(SUGAR_BEETS)
-1 AboveAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
-1 AboveAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
>= 0

c_l_AboveAverageScenario_EnforceCattleFeedRequirement(WHEAT)_:
+3 AboveAverageScenario_DevotedAcreage(WHEAT)
+1 AboveAverageScenario_QuantityPurchased(WHEAT)
-1 AboveAverageScenario_QuantitySubQuotaSold(WHEAT)
-1 AboveAverageScenario_QuantitySuperQuotaSold(WHEAT)
>= 200

c_u_AboveAverageScenario_LimitAmountSold(CORN)_:
-3.6000000000000001 AboveAverageScenario_DevotedAcreage(CORN)
+1 AboveAverageScenario_QuantitySubQuotaSold(CORN)
+1 AboveAverageScenario_QuantitySuperQuotaSold(CORN)
<= 0

c_u_AboveAverageScenario_LimitAmountSold(SUGAR_BEETS)_:
-24 AboveAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1 AboveAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
+1 AboveAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
<= 0

c_u_AboveAverageScenario_LimitAmountSold(WHEAT)_:
-3 AboveAverageScenario_DevotedAcreage(WHEAT)
+1 AboveAverageScenario_QuantitySubQuotaSold(WHEAT)
+1 AboveAverageScenario_QuantitySuperQuotaSold(WHEAT)
<= 0

r_l_AboveAverageScenario_EnforceQuotas(CORN)_:
+1 AboveAverageScenario_QuantitySubQuotaSold(CORN)
>= 0

r_u_AboveAverageScenario_EnforceQuotas(CORN)_:
+1 AboveAverageScenario_QuantitySubQuotaSold(CORN)
<= 100000

r_l_AboveAverageScenario_EnforceQuotas(SUGAR_BEETS)_:
+1 AboveAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
>= 0

r_u_AboveAverageScenario_EnforceQuotas(SUGAR_BEETS)_:
+1 AboveAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
<= 6000

r_l_AboveAverageScenario_EnforceQuotas(WHEAT)_:
+1 AboveAverageScenario_QuantitySubQuotaSold(WHEAT)
>= 0

r_u_AboveAverageScenario_EnforceQuotas(WHEAT)_:
+1 AboveAverageScenario_QuantitySubQuotaSold(WHEAT)
<= 100000

c_e_ONE_VAR_CONSTANT: 
ONE_VAR_CONSTANT = 1.0

bounds
    -inf <= MASTER_BLEND_VAR_RootNode(_DevotedAcreage__CORN_) <= +inf
    -inf <= MASTER_BLEND_VAR_RootNode(_DevotedAcreage__SUGAR_BEETS_) <= +inf
    -inf <= MASTER_BLEND_VAR_RootNode(_DevotedAcreage__WHEAT_) <= +inf
   0 <= BelowAverageScenario_DevotedAcreage(CORN) <= 500
   0 <= BelowAverageScenario_DevotedAcreage(SUGAR_BEETS) <= 500
   0 <= BelowAverageScenario_DevotedAcreage(WHEAT) <= 500
   0 <= BelowAverageScenario_QuantitySubQuotaSold(CORN) <= +inf
   0 <= BelowAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS) <= +inf
   0 <= BelowAverageScenario_QuantitySubQuotaSold(WHEAT) <= +inf
   0 <= BelowAverageScenario_QuantitySuperQuotaSold(CORN) <= +inf
   0 <= BelowAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS) <= +inf
   0 <= BelowAverageScenario_QuantitySuperQuotaSold(WHEAT) <= +inf
   0 <= BelowAverageScenario_QuantityPurchased(CORN) <= +inf
   0 <= BelowAverageScenario_QuantityPurchased(SUGAR_BEETS) <= +inf
   0 <= BelowAverageScenario_QuantityPurchased(WHEAT) <= +inf
   0 <= AverageScenario_DevotedAcreage(CORN) <= 500
   0 <= AverageScenario_DevotedAcreage(SUGAR_BEETS) <= 500
   0 <= AverageScenario_DevotedAcreage(WHEAT) <= 500
   0 <= AverageScenario_QuantitySubQuotaSold(CORN) <= +inf
   0 <= AverageScenario_QuantitySubQuotaSold(SUGAR_BEETS) <= +inf
   0 <= AverageScenario_QuantitySubQuotaSold(WHEAT) <= +inf
   0 <= AverageScenario_QuantitySuperQuotaSold(CORN) <= +inf
   0 <= AverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS) <= +inf
   0 <= AverageScenario_QuantitySuperQuotaSold(WHEAT) <= +inf
   0 <= AverageScenario_QuantityPurchased(CORN) <= +inf
   0 <= AverageScenario_QuantityPurchased(SUGAR_BEETS) <= +inf
   0 <= AverageScenario_QuantityPurchased(WHEAT) <= +inf
   0 <= AboveAverageScenario_DevotedAcreage(CORN) <= 500
   0 <= AboveAverageScenario_DevotedAcreage(SUGAR_BEETS) <= 500
   0 <= AboveAverageScenario_DevotedAcreage(WHEAT) <= 500
   0 <= AboveAverageScenario_QuantitySubQuotaSold(CORN) <= +inf
   0 <= AboveAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS) <= +inf
   0 <= AboveAverageScenario_QuantitySubQuotaSold(WHEAT) <= +inf
   0 <= AboveAverageScenario_QuantitySuperQuotaSold(CORN) <= +inf
   0 <= AboveAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS) <= +inf
   0 <= AboveAverageScenario_QuantitySuperQuotaSold(WHEAT) <= +inf
   0 <= AboveAverageScenario_QuantityPurchased(CORN) <= +inf
   0 <= AboveAverageScenario_QuantityPurchased(SUGAR_BEETS) <= +inf
   0 <= AboveAverageScenario_QuantityPurchased(WHEAT) <= +inf
end
