from django.shortcuts import render, redirect, get_object_or_404
from .models import DataFile, Transaction
from .forms import UploadForm, TransferForm
from django.contrib.auth.decorators import login_required
import time
from .BlockChain import BlockChain
from .Transaction import transaction
import hashlib
import ast
from .Block import Block

blockchain = BlockChain()

def construct_transaction(transaction_info):
    new_transaction = transaction(transaction_info['filename'],
                                  transaction_info['uploader'],
                                  transaction_info['hash'],
                                  transaction_info['timestamp'],
                                  transaction_info['pre_owner'],
                                  transaction_info['current_owner'],
                                  transaction_info['trans_type'])
    return new_transaction

def construct_block(block_info):
    block = Block(block_info['timestamp'],
                  [construct_transaction(block_info['transactions'])],
                  block_info['previous_hash'])
    block.nonce = block_info['nonce']
    block.hash = block_info['hash']
    return block

with open("Transaction.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        if line is not None:
            block_info = ast.literal_eval(line)
            new_block = construct_block(block_info)
            blockchain.chain.append(new_block)



@login_required
def home(request):
    files = DataFile.objects.all()
    return render(request, 'core/home.html', {'files': files})

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            datafile = form.save(commit=False)
            datafile.uploader = request.user
            datafile.current_owner = request.user
            datafile.save()

            file_content = request.FILES['file'].read()
            file_hash = hashlib.sha256(file_content).hexdigest()

            block_data = {
                'filename': datafile.title,
                'uploader': request.user.username,
                'hash': file_hash,
                'timestamp': str(time.time()),
                'pre_owner': 'NULL',
                'current_owner': request.user.username,
                'trans_type': 'upload'
            }

            blockchain.add_transaction(transaction(block_data['filename'], block_data['uploader'], block_data['hash'], block_data['timestamp']
                                                   , block_data['pre_owner'], block_data['current_owner'], block_data['trans_type']))
            blockchain.mine_pending_transaction()
            block = blockchain.get_latest_block()
            print(f'previous_hash: {block.previous_hash}')
            print(f'timestamp: {block.timestamp}')
            print(f'hash: {block.hash}')
            print('')

            return redirect('home')
    else:
        form = UploadForm()
    return render(request, 'core/upload.html', {'form': form})

@login_required
def detail(request, file_id):
    datafile = get_object_or_404(DataFile, pk=file_id)
    return render(request, 'core/detail.html', {'datafile': datafile})

@login_required
def search_transactions(request):
    query = request.GET.get('search', '')
    results = []

    if query:
        with open("Transaction.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if line is not None:
                    record = ast.literal_eval(line.strip())
                    tx = record['transactions']
                    filename = record['transactions']['filename']
                    if query == filename:
                        results.append(tx)

    return render(request, 'core/search_transactions.html', {
        'query': query,
        'results': results
    })

@login_required
def buy_file(request, file_id):
    datafile = get_object_or_404(DataFile, pk=file_id)
    if datafile.is_for_sale and datafile.current_owner != request.user:
        Transaction.objects.create(
            buyer=request.user,
            seller=datafile.current_owner,
            datafile=datafile,
            price=datafile.price
        )

        block_data = {
            'filename': datafile.title,
            'uploader': datafile.uploader.username,
            'hash': 'NULL',
            'timestamp': str(time.time()),
            'pre_owner': datafile.current_owner.username,
            'current_owner': request.user.username,
            'trans_type': 'buy_file'
        }

        datafile.current_owner = request.user
        datafile.is_for_sale = False

        blockchain.add_transaction(
            transaction(block_data['filename'], block_data['uploader'], block_data['hash'], block_data['timestamp']
                        , block_data['pre_owner'], block_data['current_owner'], block_data['trans_type']))
        blockchain.mine_pending_transaction()
        block = blockchain.get_latest_block()
        print(f'previous_hash: {block.previous_hash}')
        print(f'timestamp: {block.timestamp}')
        print(f'hash: {block.hash}')
        print('')

        datafile.save()
    return redirect('home')

@login_required
def transfer_ownership(request, file_id):
    datafile = get_object_or_404(DataFile, pk=file_id, current_owner=request.user)
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():

            block_data = {
                'filename': datafile.title,
                'uploader': datafile.uploader.username,
                'hash': 'NULL',
                'timestamp': str(time.time()),
                'pre_owner': datafile.current_owner.username,
                'current_owner': form.cleaned_data['new_owner'].username,
                'trans_type': 'transfer'
            }

            new_owner = form.cleaned_data['new_owner']
            datafile.current_owner = request.user
            datafile.is_for_sale = False

            blockchain.add_transaction(
                transaction(block_data['filename'], block_data['uploader'], block_data['hash'], block_data['timestamp']
                            , block_data['pre_owner'], block_data['current_owner'], block_data['trans_type']))
            blockchain.mine_pending_transaction()
            block = blockchain.get_latest_block()
            print(f'previous_hash: {block.previous_hash}')
            print(f'timestamp: {block.timestamp}')
            print(f'hash: {block.hash}')
            print('')

            datafile.current_owner = new_owner
            datafile.save()
            return redirect('home')
    else:
        form = TransferForm()
    return render(request, 'core/transfer.html', {'form': form, 'datafile': datafile})

