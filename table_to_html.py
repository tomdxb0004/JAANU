from send_email import send_mail
from pretty_html_table import build_table


def send_dataframe(best_picks_dataframe):
    output = build_table(best_picks_dataframe, 'blue_light')
    send_mail(output)
    return "Mail sent successfully."


 