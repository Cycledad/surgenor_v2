select purchaser.purchaserName,
purchaseOrderNbr,
orderNbr,
s.supplierName,
part.partNbr,
part.partDesc,
o.OrderQuantity,
o.OrderPartPrice,
o.OrderTotalCost
from purchaseOrder p, OrderTbl o, supplier s, Part, Purchaser
where p.purchaseOrderNbr = o.orderNbr
AND o.OrderSupplierId = s.id
and o.OrderPartId = part.id
and Purchaser.id = p.purchaseOrderPurchaserId