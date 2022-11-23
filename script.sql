drop table if exists Branch cascade; 
drop table if exists Customer cascade; 
drop table if exists Employee cascade; 
drop table if exists Loan cascade; 
drop table if exists Account cascade; 
drop table if exists Transaction cascade; 

create table Branch
(
	branch_id	int		UNIQUE,
	address		varchar(50),
	primary key (branch_id)
);

create table Customer
(
	customer_id	int		UNIQUE,
	name		varchar(30)	NOT NULL,
	address		varchar(50),
	branch_id	int,
	primary key (customer_id),
	foreign key (branch_id) references Branch on delete cascade
);

create table Employee 
(
	emp_id		int		UNIQUE, 
	name		varchar(30) NOT NULL,
	branch_id	int,
	address		varchar(50), 
	salary		numeric(10,2), 
	ssn			int		UNIQUE, 
	type		varchar(15)		check (type = 'teller' or type = 'loan_specialist' or type = 'manager'),
	primary key (emp_id, ssn), 
	foreign key (branch_id) references Branch on delete cascade
);

create table Loan
(
	loan_id		int		UNIQUE, 
	amount		numeric(10,2),
	runtime		int,
	interest_schedule	varchar(50), 
	customer_id	int,
	primary key (loan_id),
	foreign key (customer_id) references Customer on delete cascade
);

create table Account
(
	account_id	int		UNIQUE,
	type		varchar(20)	check (type = 'checking' or type = 'saving'),
	balance		numeric(10,2),
	customer_id	int,
	primary key (account_id),
	foreign key (customer_id) references Customer on delete cascade
);

create table Transaction
(
	transaction_id	int	UNIQUE, 
	description	varchar(300),
	amount		numeric(10,2) NOT NULL,
	type		varchar(20)		check (type = 'deposit' or type = 'withdrawal' or type = 'transfer'),
	account_id	int,
	primary key (transaction_id),
	foreign key (account_id) references Account on delete cascade
);
