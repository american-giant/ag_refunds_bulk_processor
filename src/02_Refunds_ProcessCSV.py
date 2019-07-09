import stripe
import csv

# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
# stripe.api_key = "sk_test_rfOkk13hmtpeXwQJT64ZAr48"
stripe.api_key = "INSERT_LIVE_SECRET_KEY" # DO NOT COMMIT LIVE SECRET KEY TO GITHUB REPO!

# Configure input and output
data_directory = 'data/'
refund_list_file_name = data_directory + 'refunds.csv'
refund_log_file_name = data_directory + 'refunds.log'
refund_status_file_name = data_directory + 'refunds_status.csv'

fields = []
rows = []

# Reading csv file
with open(refund_list_file_name, 'r') as csvfile:
    # Creating a csv reader object
    csvreader = csv.reader(csvfile)

    # Extracting field names in the first row
    fields = csvreader.__next__

    #Extracing each data row one by one
    for row in csvreader:
        rows.append(row)

    refunds = rows

# Output details about the refunds
def super_print(log_file, output_string):
  '''Print to log and to the console.'''
  print(output_string)
  log_file.write(output_string)

# Create output file object in writing mode
log_file = open(refund_log_file_name, 'w')

# Process each refund, one by one, may take a long time.
for refund in refunds[1:]:

    # Generate details for refund that's about to occur
    order_no = "Processing refund for Order Number: " + refund[0] + '\n'
    amount = "For the amount of: " + str(int(round(float(refund[6]), 2) * 100)) + ' cents USD\n'
    charge_id = "Using the charge ID of: " + refund[7] + '\n'
    output_string = order_no + amount + charge_id

    # Output pre-request string
    super_print(log_file, output_string)

    # Try to refund, if it fails a message will be printed indicating that.
    # Only attempts to process via Stripe Refund API. Non-Stripe Refunds will fail (PayPal, Other).
    try:
        # Actual refund
        response = stripe.Refund.create(
            charge=refund[7],
            amount=int(round(float(refund[6]), 2) * 100),
            reason="requested_by_customer",
        )
        response = "PROCESSED PROPERLY!\n"
        status = "SUCCESS"
    except:
        response = "***********FAILED TO PROCESS***********\n"
        status = "FAILED"

    refund.append(status)

    # Output post-request string
    super_print(log_file, response)

# Close output file
log_file.close()

# Refund Status CSV File Header
refund_status_fields = ["Order Number", "Order Status", "Shipping Status", "RMA Number", "RMA Status", "Return Date", "Refund Amount", "Stripe Charge ID", "PayPal Transaction ID", "STATUS"]

# Write to Refund Status CSV File
with open(refund_status_file_name, 'w', newline='') as csv_statusfile:
    # Create a csv writer object
    csvwriter = csv.writer(csv_statusfile)

    # Write the fields
    csvwriter.writerow(refund_status_fields)

    for refund in refunds[1:]:
        # Write the data rows
        csvwriter.writerow([refund[0],refund[1],refund[2],refund[3],refund[4],refund[5],refund[6],refund[7],refund[8],refund[9]])
