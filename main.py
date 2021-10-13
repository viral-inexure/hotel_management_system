
    # def calculate_amount(self):
    #     reservation_start_date = self.check_out - self.check_in
    #     print('res_start_date', reservation_start_date)
    #     total_time = reservation_start_date.days
    #     print('total_time', total_time)
    #     a = self.check_out - self.check_in
    #     print('rate', self.room.rate)
    #     v = a.days * self.room.rate
    #     print('value', abs(v))
    #     print('days', a.days)
    #     return f'{v} for {a.days}'


# class Payment(models.Model):
#     reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
#     payment_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.reservation.username.username
#
#     def charge(self):
#         if self.reservation.check_out_done:
#             if self.reservation.check_in == self.reservation.check_out:
#                 return self.reservation.room.rate
#             else:
#                 time_delta = self.reservation.check_in - self.reservation.check_out
#                 total_time = time_delta.days
#                 total_cost = total_time * self.reservation.room.rate
#                 return abs(total_cost)
#         else:
#             return 'payment count is pending'

# class CheckPayments(models.Model):
#     reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#
#     def __str__(self):
#         return self.reservation.username.username
#
#     def calculate_amount(self):
#         reservation_start_date = self.reservation.check_out - self.reservation.check_in
#         # print('res_start_date', reservation_start_date)
#         total_time = reservation_start_date.days
#         # print('total_time', total_time)
#         a = self.end_date - self.start_date
#         # print('rate', self.reservation.room.rate)
#         v = a.days * self.reservation.room.rate
#         # print('value', abs(v))
#         # print('days', a.days)
#         return f'{v} for {a.days}'