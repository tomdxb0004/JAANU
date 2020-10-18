from send_email import send_mail
from pretty_html_table import build_table


def send_dataframe(best_picks_dataframe,table_color):
    output = build_table(best_picks_dataframe,table_color )
    send_mail(output)
    return "Mail sent successfully."


 