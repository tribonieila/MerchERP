SELECT [document_register_no],[document_register_date], [supp_sub_code],[supp_name], [location_name],[mode_of_shipment],[invoice_no],[invoice_date],[estimated_time_of_arrival],
[total_amount_in_qr],[invoice_amount],[trade_terms],[mnemonic],[cil_no],[forwarder_name],[due_date],[exchange_rate],[commodity],[payment_category],[bank_name] FROM [m3rch_inv_db].[dbo].[Document_Register] 
INNER JOIN [m3rch_inv_db].[dbo].[Supplier_Master] ON [m3rch_inv_db].[dbo].[Document_Register].[supplier_code_id] = [m3rch_inv_db].[dbo].[Supplier_Master].[id]
INNER JOIN [m3rch_inv_db].[dbo].[Location] ON [m3rch_inv_db].[dbo].[Document_Register].[location_code_id] = [m3rch_inv_db].[dbo].[Location].[id]
INNER JOIN [m3rch_inv_db].[dbo].[Supplier_Trade_Terms] ON [m3rch_inv_db].[dbo].[Document_Register].[trade_terms_id] = [m3rch_inv_db].[dbo].[Supplier_Trade_Terms].[id]
INNER JOIN [m3rch_inv_db].[dbo].[Currency] ON [m3rch_inv_db].[dbo].[Document_Register].[currency_id] = [m3rch_inv_db].[dbo].[Currency].[id]
INNER JOIN [m3rch_inv_db].[dbo].[Forwarder_Supplier] ON [m3rch_inv_db].[dbo].[Document_Register].[forwarder_supplier_id] = [m3rch_inv_db].[dbo].[Forwarder_Supplier].[id]
INNER JOIN [m3rch_inv_db].[dbo].[Payment_Category_Group] ON [m3rch_inv_db].[dbo].[Document_Register].[payment_category_id] = [m3rch_inv_db].[dbo].[Payment_Category_Group].[id]
INNER JOIN [m3rch_inv_db].[dbo].[Bank_Master] ON [m3rch_inv_db].[dbo].[Document_Register].[bank_master_id] = [m3rch_inv_db].[dbo].[Bank_Master].[id]