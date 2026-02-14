from pathlib import Path
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from Planilha import Planilha

class Cpus(Planilha):
    
    def __init__(self, 
                 path: Path, 
                 wb_orig_name: str, 
                 ws_orig_name: str, 
                 wb_dest: Workbook,
                 ws_dest: Worksheet
    ) -> None:
        
        super().__init__(path, wb_orig_name, ws_orig_name, wb_dest, ws_dest)

    def delete_data(self) -> bool:
        ws = self._ws_dest
        last_row = self._get_last_row_in_column(ws, "J")

        if last_row >= 7:
            ws.delete_rows(7, last_row - 6)
            return True

        return False