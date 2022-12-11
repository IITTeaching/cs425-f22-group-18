drop table if exists Address cascade;
drop table if exists Branch cascade; 
drop table if exists Customer cascade; 
drop table if exists Account cascade; 
drop table if exists Employee cascade; 
drop table if exists Transactions cascade;
drop table if exists TransferInformation cascade; 
drop table if exists ExternalInformation cascade; 


create table Address
(
	address_id 		varchar(10),
	city 			varchar(20),
	state 			varchar(20),
	zip 			char(5),
	primary key (address_id)
);


create table Branch
(
	branch_id		varchar(15),
	address_id 		varchar(10),
	status 			varchar(8) check (Status='Active' or Status='Closed'),
	primary key (branch_id), 
	foreign key (address_id) references Address
);


create table Customer
(
	customer_id		varchar(15),
	name			varchar(20),
	password		varchar(12),
	branch_id		varchar(15),
	address_id		varchar(15),
	primary key (customer_id),
	foreign key (branch_id) references Branch, 
	foreign key (address_id) references Address
);


create table Employee
(
	employee_id 	varchar(15),
	name 			varchar(50),
	password 		varchar(12),
	ssn 			char(9),
	position 		varchar(9) check (position = 'Manager' or position = 'Teller'),
	salary 			numeric(11,2),
	branch_Id 		varchar(15),
	address_id 		varchar(15),
	primary key (employee_id),
	foreign key (address_id) references Address, 
	foreign key (branch_id) references Branch
);


create table Account
(
	account_id 		varchar(15),
	balance 		numeric(11,2),
	type 			varchar(10) check (type = 'Saving' or type = 'Checking'),
	customer_id 	varchar(15),
	status 			varchar(8) check (status = 'Active' or Status = 'Closed'),
	primary key (account_id),
	foreign key (customer_id) references Customer
	
);


create table Transactions
(
	transaction_id 	varchar(15),
	amount 			numeric(11,2),
	description 	varchar(100),
	type 			varchar(20) check (Type = 'Deposit' or Type = 'Withdrawl' or Type = 'Transfer' or Type = 'ExternalTransfer'),
	customer_id 	varchar(15),
	employee_id 	varchar(15),
	balance_from 	numeric(11,2),
	balance_to 		numeric(11,2) default NULL,
	den				date default current_timestamp,
	primary key (transaction_id)
);


create table TransferInformation
(
	transaction_id	varchar(15),
	from_account 	varchar(15) references Account(Account_Id),
	to_account 		varchar(15) references Account(Account_Id),
	primary key (transaction_id, from_account, to_account),
	foreign key (transaction_id) references Transactions
);


create table ExternalInformation
(
	transaction_id 	varchar(15),
	from_account 	varchar(15) references Account(Account_Id),
	bank 			varchar(20),
	account_number 	char(12),
	routing_number 	char(9),
	primary key (transaction_id, from_account, bank, account_number, routing_number),
	foreign key (transaction_id) references Transactions
);


insert into Address values ('1', 'Chicago', 'IL', '60616');
insert into Address values ('2', 'San-Francisco', 'CA', '31415');
insert into Address values ('3', 'New York', 'NY', '12011');

insert into Branch values ('1', '1', 'Active');
insert into Branch values ('2', '2', 'Active');
insert into Branch values ('3', '3', 'Active');

insert into Customer values ('1', 'Stas', '1234567890', '1', '1');

insert into Employee values ('1', 'John Doe', '1234567890', '123456789', 'Manager', 130000.00, '1', '1');
insert into Employee values ('2', 'Jane Doe', '0987654321', '987654321', 'Teller', 45000.00, '2', '2');
